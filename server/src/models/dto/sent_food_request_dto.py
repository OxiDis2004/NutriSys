from uuid import UUID

from pydantic import BaseModel, Field

class SentFoodRequestDTO(BaseModel):
    user_id: UUID | None = Field(..., max_length=36)
    image_path: str = Field(
        ...,
        max_length=300,
        pattern=r"^[a-zA-Z0-9_\/:]+$"
    )