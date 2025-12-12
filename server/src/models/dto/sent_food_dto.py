from pydantic import BaseModel

class SentFoodDTO(BaseModel):
    image_path: str