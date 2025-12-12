from pydantic import BaseModel


class WaterRequestDTO(BaseModel):
    user_id: str | None = None
    drunk_water: int = 0