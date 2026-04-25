from uuid import UUID

from pydantic import BaseModel, Field, field_serializer


class UserDTO(BaseModel):
    id: UUID | None = Field(None, description="Unique user identifier")
    telegram_id: int | None = Field(None, description="Telegram ID as numeric")
    language: str | None = Field(
        None,
        min_length=2,
        max_length=2,
        pattern=r"^[a-z]{2}$",
        description="User language code (ISO 639-1)",
    )

    @property
    def user_id(self):
        return str(self.id)

    @field_serializer("id")
    def serialize_id(self, id: UUID | None) -> str | None:
        return str(id) if id is not None else None
