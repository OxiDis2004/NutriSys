from pydantic import BaseModel, Field
from uuid import UUID


class UserDTO(BaseModel):
    id: UUID | None = Field(..., description="Unique user identifier")
    telegram_id: int | None = Field(
        ...,
        description="Telegram ID as numeric string"
    )
    language: str | None = Field(
        ...,
        max_length=2,
        pattern=r"^[a-z]{2}$",
        description="User language code (ISO 639-1)"
    )

    @property
    def user_id(self) -> str:
        return str(self.id)
