from collections import defaultdict
from datetime import date

from src.models.language import Language
from src.models.user import User
from src.services import request_get, request_put, request_post, ServerEndpoint

USERS = defaultdict()
USERS_CALORIE = {}

def get_current_user(telegram_id: int) -> User | None:
    return USERS.get(telegram_id, None)

def add_user(row):
    telegram_id = row.get('telegram_id', None)
    if telegram_id is not None:
        user = User()
        user.user_id = row.get('id', None)
        user.telegram_id = telegram_id
        user.language = row.get('language', Language.ENGLISH)
        update_user(telegram_id, user)

async def get_all_users():
    data = (await request_get(ServerEndpoint.USERS.value)).json()
    for row in data:
        add_user(row)

async def user_request(request_method, url: ServerEndpoint, telegram_id: int) -> bool:
    user = get_current_user(telegram_id)

    if user is None:
        body = User(None, telegram_id).base_info()
        response = await request_method(url.value, body, False)
        if response.status_code == 200:
            data = response.json()
            add_user(data)
        else:
            return False

    return True

async def login_user(telegram_id: int):
    return await user_request(request_post, ServerEndpoint.LOGIN, telegram_id)

async def register_user(telegram_id: int):
    return await user_request(request_put, ServerEndpoint.REGISTER, telegram_id)

async def is_user_exists(telegram_id: int):
    return get_current_user(telegram_id) is not None

def update_user(telegram_id: int, user: User):
    USERS[telegram_id] = user

def get_current_day():
    return date.today().strftime("%Y-%m-%d")

def set_user_calorie(telegram_id: int, calorie: int):
    curr_day = get_current_day()
    user_calorie = USERS_CALORIE.get(telegram_id, {})
    total_calorie = user_calorie.get(curr_day, 0)
    user_calorie.update({ curr_day: total_calorie + calorie})
    USERS_CALORIE.update({ telegram_id: user_calorie })

def get_user_calorie(telegram_id: int, curr_day: str = get_current_day()):
    return USERS_CALORIE.get(telegram_id, {}).get(curr_day, 0)

def get_website_url(telegram_id: int):
    user = get_current_user(telegram_id)
    return "https://google.com"