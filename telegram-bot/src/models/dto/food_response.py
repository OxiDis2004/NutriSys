from dataclasses import dataclass


@dataclass
class FoodResponseDTO:
    day: str = None
    name: str = None
    calorie: int = None
    protein: float = None
    carbon: float = None
    fat: float = None