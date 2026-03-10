from uuid import UUID

from pydantic import BaseModel, Field


class WaterRequestDTO(BaseModel):
    user_id: UUID = Field(..., description="Unique user identifier")
    drunk_water: int = Field(..., description="Users drunk water now")