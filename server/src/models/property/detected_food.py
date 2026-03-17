from pydantic import BaseModel


class DetectedFood(BaseModel):
    label: str | None = None
    mass: int | None = None