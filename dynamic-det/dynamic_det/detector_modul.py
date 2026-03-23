from __future__ import annotations

import io
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import cv2
import numpy as np
import torch
import torch.nn as nn
from PIL import Image

from dynamic_det.models.yolo import Model
from dynamic_det.utils.general import check_img_size, non_max_suppression, scale_coords
from dynamic_det.utils.torch_utils import intersect_dicts

@dataclass
class DetectionResult:
    name: str
    confidence: float
    bbox: List[float]  # [x1, y1, x2, y2]
    class_id: int

class DetectorModul:
    def __init__(
            self,
            cfg_path: str,
            weights_path: str,
            num_classes: int = '',
            device: str = "cuda:0",
            img_size: int = 640,
            conf_thres: float = 0.25,
            iou_thres: float = 0.65,
            dy_thres: float = 0.5,
            class_names: Optional[List[str]] = None,
            agnostic_nms: bool = False,
            classes: Optional[List[int]] = None,
    ) -> None:
        self.cfg_path = cfg_path
        self.weights_path = weights_path
        self.num_classes = num_classes
        self.device = torch.device(
            device if torch.cuda.is_available() or device == "cpu" else "cpu"
        )
        self.img_size = img_size
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.dy_thres = dy_thres
        self.agnostic_nms = agnostic_nms
        self.classes = classes

        self.half = self.device.type != "cpu"
        self.model = self._load_model(weights_path)
        self.names = (
            class_names
            if class_names is not None
            else (self.model.module.names if hasattr(self.model, "module") else self.model.names)
        )
        self.stride = int(self.model.stride.max())
        self.img_size = check_img_size(self.img_size, s=self.stride)

        # warmup once, same idea as in detect.py
        if self.device.type != "cpu":
            dummy = torch.zeros(1, 3, self.img_size, self.img_size, device=self.device)
            dummy = dummy.half() if self.half else dummy.float()
            with torch.no_grad():
                _ = self.model(dummy)

    def _load_model(self, weights_path: str) -> nn.Module:
        model = Model(self.cfg_path, ch=3, nc=self.num_classes)

        checkpoint = torch.load(weights_path, map_location="cpu", weights_only=False)
        state_dict = checkpoint["model"] if isinstance(checkpoint, dict) and "model" in checkpoint else checkpoint
        state_dict = intersect_dicts(state_dict, model.state_dict())
        model.load_state_dict(state_dict, strict=False)

        model.to(self.device)

        for p in model.parameters():
            p.requires_grad = False

        model.float().fuse().eval()

        # compatibility updates copied from detect.py logic
        for m in model.modules():
            if type(m) in [nn.Hardswish, nn.LeakyReLU, nn.ReLU, nn.ReLU6, nn.SiLU]:
                m.inplace = True
            elif type(m) is nn.Upsample:
                m.recompute_scale_factor = None

        if hasattr(model, "dy_thres"):
            model.dy_thres = self.dy_thres

        if self.half:
            model.half()

        return model

    def _letterbox(
            self,
            image: np.ndarray,
            new_shape: int | tuple[int, int] = 640,
            color: tuple[int, int, int] = (114, 114, 114),
            auto: bool = True,
            scale_fill: bool = False,
            scaleup: bool = True,
            stride: int = 32,
    ) -> tuple[np.ndarray, tuple[float, float], tuple[float, float]]:
        """
        Same preprocessing idea used by YOLO-style loaders.
        """
        shape = image.shape[:2]  # (h, w)

        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)

        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        if not scaleup:
            r = min(r, 1.0)

        ratio = (r, r)
        new_unpad = (int(round(shape[1] * r)), int(round(shape[0] * r)))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]

        if auto:
            dw, dh = np.mod(dw, stride), np.mod(dh, stride)
        elif scale_fill:
            dw, dh = 0.0, 0.0
            new_unpad = (new_shape[1], new_shape[0])
            ratio = (new_shape[1] / shape[1], new_shape[0] / shape[0])

        dw /= 2
        dh /= 2

        if shape[::-1] != new_unpad:
            image = cv2.resize(image, new_unpad, interpolation=cv2.INTER_LINEAR)

        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))

        image = cv2.copyMakeBorder(
            image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color
        )
        return image, ratio, (dw, dh)

    def preprocess_image(self, image_bytes: bytes) -> tuple[torch.Tensor, np.ndarray]:
        """
        Returns:
          tensor: shape [1, 3, H, W]
          original_bgr: original image in OpenCV BGR format for coordinate rescaling
        """
        pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        rgb = np.array(pil_img)
        bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

        resized, _, _ = self._letterbox(bgr, new_shape=self.img_size, stride=self.stride)

        # BGR -> RGB, HWC -> CHW
        img = resized[:, :, ::-1].transpose(2, 0, 1)
        img = np.ascontiguousarray(img)

        tensor = torch.from_numpy(img).to(self.device)
        tensor = tensor.half() if self.half else tensor.float()
        tensor /= 255.0

        if tensor.ndimension() == 3:
            tensor = tensor.unsqueeze(0)

        return tensor, bgr

    def postprocess(
            self,
            raw_output: torch.Tensor,
            tensor_shape: torch.Size,
            original_image: np.ndarray,
    ) -> List[Dict[str, Any]]:
        pred = non_max_suppression(
            raw_output,
            self.conf_thres,
            self.iou_thres,
            classes=self.classes,
            agnostic=self.agnostic_nms,
        )

        results: List[Dict[str, Any]] = []

        for det in pred:
            if len(det):
                det[:, :4] = scale_coords(
                    tensor_shape[2:], det[:, :4], original_image.shape
                ).round()

                for *xyxy, conf, cls in reversed(det):
                    class_id = int(cls)
                    results.append(
                        {
                            "name": self.names[class_id],
                            "confidence": float(conf),
                            "bbox": [float(x) for x in xyxy],
                            "class_id": class_id,
                        }
                    )

        return results

    def predict(self, image_bytes: bytes) -> List[Dict[str, Any]]:
        tensor, original_image = self.preprocess_image(image_bytes)

        with torch.no_grad():
            raw_output = self.model(tensor)[0]

        return self.postprocess(raw_output, tensor.shape, original_image)
