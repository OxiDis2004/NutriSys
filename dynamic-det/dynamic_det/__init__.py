from pathlib import Path

from dynamic_det.detector_modul import DetectorModul

def detector():
    base_dir = Path(__file__).resolve().parent
    cfg_path = base_dir / "cfg" / "dy-yolov7x-step2.yaml"
    weights_path = base_dir / "weights" / "dy-yolov7x.pt"

    return DetectorModul(
        str(cfg_path),
        str(weights_path)
    )
