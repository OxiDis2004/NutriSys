import datetime

from pydantic import BaseModel


class StatisticRequestDTO(BaseModel):
    user_id: str | None = None
    date_from: datetime.date | None = None
    date_to: datetime.date | None = None