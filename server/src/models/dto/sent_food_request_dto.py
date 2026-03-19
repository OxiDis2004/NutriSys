from uuid import UUID

from pydantic import BaseModel, Field
from starlette.datastructures import UploadFile


class SentFoodRequestDTO(BaseModel):
    user_id: UUID | None = Field(..., max_length=36)
    image: UploadFile = File(...)
