from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.builders.menu_builder import MenuFactory
from src.handlers import history_append
from src.models.menu_parts.menu_type import MenuType
from src.services.users import register_user, login_user, is_exists_user

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    if not await is_exists_user(state):
        success = await login_user(state, message.from_user.id)
        if not success:
            await register_user(state, message.from_user.id)
    menu = await MenuFactory.build_menu(MenuType.START, state)
    await message.answer(
        text=menu.title,
        reply_markup=menu.keyboard
    )
    await history_append(state, MenuType.START)
