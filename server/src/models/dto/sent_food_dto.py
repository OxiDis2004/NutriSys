from pydantic import BaseModel, Field

class SentFoodDTO(BaseModel):
    image_path: str = Field(
        ...,
        max_length=300,
        pattern=r"^[a-zA-Z0-9_\/:]+$"
    )