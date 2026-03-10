from datetime import date

from pydantic import BaseModel, Field


class WaterResponseDTO(BaseModel):
    day: date = Field(None, description="Date")
    drunk_water: int = Field(..., description="Users drunk water at date")
