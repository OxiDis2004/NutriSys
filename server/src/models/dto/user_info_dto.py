import datetime

from pydantic import BaseModel

from src.models.property.activity import Activity
from src.models.property.goal import Goal


class UserInfoDTO(BaseModel):
    id: str | None = None
    name: str | None = None
    lastname: str | None = None
    birthday: datetime.date | None = None
    weight: int | None = None
    height: int | None = None
    sex: str | None = None
    count_of_sport_in_week: Activity | None = None
    goal: Goal | None = None