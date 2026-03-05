from src.models.language import Language
from src.models.user import User

USERS = {}
USER_WATER = {}

def get_current_user(telegram_id: int) -> User | None:
    user = USERS.get(telegram_id, None)

    if user is None:
        user = User()
        user.user_id = 1
        user.telegram_id = telegram_id
        USERS.update({ telegram_id: user })

    return user

def get_current_user_language(telegram_id: int):
    user: User = get_current_user(telegram_id)
    return user.language if user is not None and user.language is not None else Language.ENGLISH.value

def set_current_user_language(telegram_id: int, language: str):
    user: User = get_current_user(telegram_id)
    if user.language != language:
        user.language = language
        USERS.update({ telegram_id: user })

def add_water(telegram_id: int, water: int) -> int:
    user: User | None = get_current_user(telegram_id)
    add_water_to_user(user, water)
    return USER_WATER[user.telegram_id]

def add_water_to_user(user: User, water: int):
    total_water = USER_WATER.get(user.telegram_id, 0)
    USER_WATER.update({user.telegram_id: total_water + water})
