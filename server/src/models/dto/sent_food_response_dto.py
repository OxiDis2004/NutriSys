from datetime import date

from pydantic import BaseModel, Field

from src.models.property.food_statistic import FoodStatistic


class SentFoodResponseDTO(BaseModel):
    day: date = Field(..., description="Date")
    statistic: FoodStatistic = Field(..., description="Food statistic")
