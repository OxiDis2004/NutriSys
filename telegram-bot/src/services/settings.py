from aiogram.fsm.context import FSMContext

from src.models.user import User
from src.services import request_put, ServerEndpoint
from src.services.users import get_user_id, get_current_language, update_user


async def set_current_language(state: FSMContext, language: str):
    curr_language = await get_current_language(state)
    if curr_language != language:
        user_id = await get_user_id(state)
        body = User.static_base_info(user_id, language=language)
        resp = await request_put(ServerEndpoint.CHANGE_LANGUAGE.value, body)
        if resp.status_code == 202:
            await update_user(state, user_id, language)

async def new_update_user_info(state: FSMContext, **kwargs):
    user_id = await get_user_id(state)
    body = User.static_extension_info(user_id, **kwargs)
    resp = await request_put(ServerEndpoint.UPDATE_INFO.value, body)
    return resp.status_code == 202
