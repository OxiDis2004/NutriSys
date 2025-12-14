from datetime import date
from uuid import UUID
from pydantic import BaseModel, Field


class StatisticRequestDTO(BaseModel):
    user_id: UUID = Field(..., description="User identifier")
    date_from: date = Field(..., description="Start date for statistics")
    date_to: date = Field(..., description="End date for statistics")