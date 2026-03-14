from collections import defaultdict
from datetime import date
from uuid import uuid4

from src.models.language import Language
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.user import User
from src.services import request_get, request_put
from src.services.water import water_add_request

USERS = defaultdict()
USERS_CALORIE = {}

async def get_all_users():
    data = (await request_get("user/all_users")).json()
    for row in data:
        telegram_id = row.get('telegram_id', None)
        user = User(
            row.get('id', uuid4()),
            telegram_id,
            row.get('language', Language.ENGLISH)
        )
        if telegram_id is not None:
            USERS[telegram_id] = user

async def register_user(telegram_id: int, language: Language):
    user = get_current_user(telegram_id)

    if user is None:
        body = {
            "id": None,
            "telegram_id": telegram_id,
            "language": language.value
        }
        response = await request_put(f"/user/register", body, False)
        if response.status_code == 400:
            data = exists_user(response.json())
        else:
            data = response.json()
        user = User(
            data.get('id', uuid4()),
            data.get('telegram_id', telegram_id),
            data.get('language', language.value)
        )
        USERS[telegram_id] = user

def exists_user(data):
    return data["detail"]["user"]

def get_current_user(telegram_id: int) -> User | None:
    return USERS.get(telegram_id, None)

def get_current_user_language(telegram_id: int):
    user: User = get_current_user(telegram_id)
    return user.language if user.language is not None else Language.ENGLISH.value

async def set_current_user_language(telegram_id: int, language: str):
    user: User = get_current_user(telegram_id)
    if user.language != language:
        user.language = language
        body = {
            "id": user.user_id,
            "telegram_id": user.telegram_id,
            "language": user.language
        }
        resp = await request_put(f"/user/change_language", body)

        if resp.status_code == 202:
            USERS[telegram_id] = user

def get_current_day():
    return date.today().strftime("%Y-%m-%d")

async def add_drunk_water(telegram_id: int, water: int):
    user: User = get_current_user(telegram_id)
    return await water_add_request(user.user_id, water)

def set_user_calorie(telegram_id: int, calorie: int):
    curr_day = get_current_day()
    user_calorie = USERS_CALORIE.get(telegram_id, {})
    total_calorie = user_calorie.get(curr_day, 0)
    user_calorie.update({ curr_day: total_calorie + calorie})
    USERS_CALORIE.update({ telegram_id: user_calorie })

def get_user_calorie(telegram_id: int, curr_day: str = get_current_day()):
    return USERS_CALORIE.get(telegram_id, {}).get(curr_day, 0)

async def update_user_info(
        telegram_id: int,
        weight: str = None,
        height: str = None,
        birthday: date = None,
        sex: MenuButtonTitle = None,
        activity: MenuButtonTitle = None,
        goal: MenuButtonTitle = None
):
    user: User = get_current_user(telegram_id)
    if user is None:
        return

    user.birthday = birthday
    user.weight = weight
    user.height = height
    user.sex = sex
    user.activity = activity
    user.goal = goal



    body = {
        "id": user.user_id,
        "name": None,
        "lastname": None,
        "birthday": user.birthday,
        "weight": user.weight,
        "height": user.height,
        "sex": user.sex,
        "activity": user.activity,
        "goal": user.goal,
    }
    print(body)
    resp = await request_put(f"/user/update_info", body)

    if resp.status_code == 202:
        USERS[telegram_id] = user

def parse_data(value, parse_func):
    try:
        return parse_func(value)
    except (KeyError, ValueError):
        return None



def get_website_url(telegram_id: int):
    user = get_current_user(telegram_id)
    return "https://google.com"