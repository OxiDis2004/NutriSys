from pydantic import BaseModel


class WaterResponseDTO(BaseModel):
    drunk_water_day: int = 0