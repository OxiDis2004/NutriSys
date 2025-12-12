from decimal import Decimal

from pydantic import BaseModel


class NutrientFoodDTO(BaseModel):
    name: str = None
    calorie: int = 0
    protein: Decimal = 0.0
    carbon: Decimal = 0.0
    fat: Decimal = 0.0