from uuid import UUID

from fastapi import File, UploadFile
from pydantic import BaseModel, Field


class SentFoodRequestDTO(BaseModel):
    user_id: UUID | None = Field(..., max_length=36)
    image: UploadFile = File(...)
