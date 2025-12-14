from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field


class WaterStatisticRequestDTO(BaseModel):
    user_id: UUID = Field(..., description="Unique user identifier")
    day: date = Field(None, description="Optional day statistic")
    week: date = Field(None, description="Optional week statistic")
    month: date = Field(None, description="Optional month statistic")
    year: date = Field(None, description="Optional year statistic")
