from pydantic import BaseModel, Field
from uuid import UUID


class UserDTO(BaseModel):
    id: UUID = Field(..., description="Unique user identifier")
    telegram_id: str = Field(
        ...,
        max_length=50,
        pattern=r"^\d+$",
        description="Telegram ID as numeric string"
    )
    language: str = Field(
        ...,
        max_length=10,
        pattern=r"^[a-z]{2}$",
        description="User language code (ISO 639-1)"
    )
