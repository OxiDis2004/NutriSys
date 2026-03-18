from collections import defaultdict
from datetime import date

from aiogram.fsm.context import FSMContext

from src.models.language import Language
from src.models.user import User
from src.services import request_put, request_post, ServerEndpoint

USERS = defaultdict()
USERS_CALORIE = {}

USER_ID = "unique_user_id"
LANGUAGE_KEY = "unique_language_key"
CALORIE_ID = "unique_calorie_id"

async def get_user_id(state: FSMContext) -> str | None:
    return await state.get_value(USER_ID, None)

async def get_current_language(state: FSMContext):
    language = (await state.get_value(LANGUAGE_KEY, None))
    return language if language is not None else Language.ENGLISH.value

async def update_user(state: FSMContext, user_id: str, language: str):
    await state.update_data(**{USER_ID: user_id, LANGUAGE_KEY: language})

async def is_exists_user(state: FSMContext):
    return (await get_user_id(state)) is not None

async def user_request(state: FSMContext, telegram_id: int, request_method, url: ServerEndpoint) \
        -> bool:
    user_id = await get_user_id(state)

    if user_id is None:
        body = User.static_base_info(user_id, telegram_id)
        response = await request_method(url.value, body, False)
        if response.status_code == 200:
            data = response.json()
            await update_user(state, data.get('id', user_id), data.get('language', Language.ENGLISH.value))
        else:
            return False

    return True

async def login_user(state: FSMContext, telegram_id: int):
    return await user_request(state, telegram_id, request_post, ServerEndpoint.LOGIN)

async def register_user(state: FSMContext, telegram_id: int):
    return await user_request(state, telegram_id, request_put, ServerEndpoint.REGISTER)

def get_current_day():
    return date.today().isoformat()

async def set_user_calorie(state: FSMContext, calorie: int):
    curr_day = get_current_day()
    total_calorie = await get_user_calorie(state)
    await state.update_data(**{ CALORIE_ID: { curr_day: total_calorie + calorie } })

async def get_user_calorie(state: FSMContext, curr_day: str = get_current_day()):
    return (await state.get_value(CALORIE_ID, {})).get(curr_day, 0)

async def get_website_url(state: FSMContext):
    user_id = await get_user_id(state)
    return "https://google.com"