from datetime import date

from pydantic import BaseModel


class WaterStatisticRequestDTO(BaseModel):
    user_id: str = None
    day: date | None = None
    week: date | None = None
    month: date | None = None
    year: date | None = None