from pydantic import BaseModel


class UserDTO(BaseModel):
    id: str | None = None
    telegram_id: str | None = None
    language: str | None = None
