from dataclasses import dataclass


@dataclass
class DetectionResult:
    name: str
    confidence: float
    bbox: list[float]  # [x1, y1, x2, y2]
    class_id: int
