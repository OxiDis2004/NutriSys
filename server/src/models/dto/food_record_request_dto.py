from uuid import UUID

from fastapi import File, UploadFile
from pydantic import BaseModel, Field


class FoodRecordRequestDTO(BaseModel):
    user_id: UUID = Field(...)
    image: UploadFile = File(...)
