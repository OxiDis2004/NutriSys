from decimal import Decimal

from pydantic import BaseModel, Field


class NutrientFoodDTO(BaseModel):
    name: str = Field(..., max_length=100, pattern=r"^[a-zA-Z0-9_]+$")
    calorie: int = Field(0, ge=0, description="Calories in food")
    protein: Decimal = Field(Decimal("0.0"), ge=0, description="Protein in grams")
    carbon: Decimal = Field(Decimal("0.0"), ge=0, description="Carbohydrates in grams")
    fat: Decimal = Field(Decimal("0.0"), ge=0, description="Fat in grams")