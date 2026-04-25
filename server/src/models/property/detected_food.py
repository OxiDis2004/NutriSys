from pydantic import BaseModel


class DetectedFood(BaseModel):
    label: str = None
    mass: int = None
