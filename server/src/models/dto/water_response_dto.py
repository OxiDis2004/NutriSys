from datetime import date

from pydantic import BaseModel, Field


class WaterResponseDTO(BaseModel):
    day: date = Field(None, description="Today")
    drunk_water_day: int = Field(..., description="Users drunk water today")
