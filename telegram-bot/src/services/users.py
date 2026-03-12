from datetime import date
from uuid import uuid4

import httpx

from src.models.language import Language
from src.models.user import User
from src.services import server, request
from src.services.water import water_add_request

USERS = {}
USERS_WATER = {}
USERS_CALORIE = {}

USER_API = f"{server()}/api/user"

async def get_all_users():
    async with httpx.AsyncClient(
        headers={"Authorization": f"Bearer"}
    ) as client:
        response = await request(client.get, f"{USER_API}/all_users", None)
        data = response.json()
        for row in data:
            telegram_id = row.get('telegram_id', None)
            user = User(
                row.get('id', uuid4()),
                telegram_id,
                row.get('language', Language.ENGLISH)
            )
            if telegram_id is not None:
                USERS.update({ telegram_id: user })

async def register_user(telegram_id: int, language: Language):
    user = get_current_user(telegram_id)

    if user is None:
        async with httpx.AsyncClient() as client:
            body = {
                "id": None,
                "telegram_id": telegram_id,
                "language": language.value
            }
            response = await request(client.put, f"{USER_API}/register", body)
            data = response.json()
            user = User(
                data.get('id', uuid4()),
                data.get('telegram_id', telegram_id),
                data.get('language', Language.ENGLISH)
            )
            USERS.update({ telegram_id: user })

def get_current_user(telegram_id: int) -> User | None:
    user = USERS.get(telegram_id, None)
    return user

def get_current_user_language(telegram_id: int):
    user: User = get_current_user(telegram_id)
    if user.language is None:
        set_current_user_language(telegram_id, Language.ENGLISH.value)
    return user.language

def set_current_user_language(telegram_id: int, language: str):
    user: User = get_current_user(telegram_id)
    if user.language != language:
        user.language = language
        USERS.update({ telegram_id: user })

def get_current_day():
    return date.today().strftime("%Y-%m-%d")

async def add_drunk_water(telegram_id: int, water: int):
    user: User = get_current_user(telegram_id)
    return await water_add_request(user.user_id, water)

async def add_water_to_user(telegram_id: int, water: int):
    curr_day = get_current_day()
    user_water = USERS_WATER.get(telegram_id, {})
    total_water = user_water.get(curr_day, 0)
    user_water.update({ curr_day: total_water + water })
    USERS_WATER.update({ telegram_id: user_water })

def get_user_water(telegram_id: int, curr_day: str = get_current_day()):
    return USERS_WATER.get(telegram_id, {}).get(curr_day, 0)

def set_user_calorie(telegram_id: int, calorie: int):
    curr_day = get_current_day()
    user_calorie = USERS_CALORIE.get(telegram_id, {})
    total_calorie = user_calorie.get(curr_day, 0)
    user_calorie.update({ curr_day: total_calorie + calorie})
    USERS_CALORIE.update({ telegram_id: user_calorie })

def get_user_calorie(telegram_id: int, curr_day: str = get_current_day()):
    return USERS_CALORIE.get(telegram_id, {}).get(curr_day, 0)

def get_website_url(telegram_id):
    return "https://google.com"