import uuid
from datetime import date

from src.models.dto.user_dto import UserDTO
from src.models.dto.user_info_dto import UserInfoDTO
from src.models.property.activity import Activity
from src.models.property.goal import Goal

LANGUAGES = ("ua", "en", "de")

USER: UserDTO = UserDTO(
    id=uuid.uuid4(),
    telegram_id=123456789,
    language=LANGUAGES[0]
)

USER_INFO: UserInfoDTO = UserInfoDTO(
    id=USER.id,
    name="Denys",
    lastname="Ponomarenko",
    birthday=date(2005, 1, 6),
    weight=100,
    height=182,
    sex='m',
    count_of_sport_in_week=Activity.HighActivity,
    goal=Goal.LoseWeight
)