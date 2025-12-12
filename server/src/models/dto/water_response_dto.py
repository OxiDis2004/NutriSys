import datetime

from pydantic import BaseModel


class WaterResponseDTO(BaseModel):
    day: datetime.date = None
    drunk_water_day: int = 0