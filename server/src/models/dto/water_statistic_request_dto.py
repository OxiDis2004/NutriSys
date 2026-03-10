from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field


class WaterStatisticRequestDTO(BaseModel):
    user_id: UUID = Field(..., description="Unique user identifier")
    statistic_date: date = Field(..., description="Period")