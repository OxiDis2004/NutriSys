from datetime import date
from aiogram.fsm.context import FSMContext

from src.models.fsm_keys import FSMKeys
from src.models.language import Language
from src.models.user import User
from src.services import request_put, request_post, ServerEndpoint

async def get_user_id(state: FSMContext) -> str | None:
    return await state.get_value(FSMKeys.USER_ID.value, None)

async def get_current_language(state: FSMContext):
    language = (await state.get_value(FSMKeys.LANGUAGE_KEY.value, None))
    return language if language is not None else Language.ENGLISH.value

async def update_user(state: FSMContext, user_id: str, language: str):
    await state.update_data(**{FSMKeys.USER_ID.value: user_id, FSMKeys.LANGUAGE_KEY.value: language})

async def is_exists_user(state: FSMContext):
    return (await get_user_id(state)) is not None

async def user_request(state: FSMContext, telegram_id: int, request_method, url: ServerEndpoint) \
        -> bool:
    body = User.static_base_info(telegram_id=telegram_id)
    response = await request_method(url.value, body, False)
    if response.status_code == 200:
        data = response.json()
        await update_user(state, data.get('id', None), data.get('language', Language.ENGLISH.value))
        return True
    else:
        return False

async def login_user(state: FSMContext, telegram_id: int):
    return await user_request(state, telegram_id, request_post, ServerEndpoint.LOGIN)

async def register_user(state: FSMContext, telegram_id: int):
    return await user_request(state, telegram_id, request_put, ServerEndpoint.REGISTER)

async def get_website_url(state: FSMContext):
    user_id = await get_user_id(state)
    return "https://google.com"