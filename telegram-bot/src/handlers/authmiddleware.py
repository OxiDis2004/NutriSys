import logging

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext

from src.services.users import is_exists_user, login_user, register_user

logger = logging.getLogger(__name__)

class AuthMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        state: FSMContext = data.get('state')
        telegram_id = event.from_user.id

        logger.debug("Auth Middleware for user=%s with state=%s", telegram_id, state)

        if state and telegram_id:
            if not await is_exists_user(state):
                success = await login_user(state, telegram_id)
                if not success:
                    await register_user(state, telegram_id)

        return await handler(event, data)
