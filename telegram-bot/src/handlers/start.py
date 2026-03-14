from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.builders.menu_builder import MenuBuilder
from src.handlers import history_append
from src.models.language import Language
from src.models.menu_parts.menu_type import MenuType
from src.services.users import register_user, is_user_exists, login_user

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    menu = MenuBuilder.build_menu(MenuType.START, message.from_user.id)
    if not await is_user_exists(message.from_user.id):
        success = await login_user(message.from_user.id, Language.ENGLISH)
        if not success:
            await register_user(message.from_user.id, Language.ENGLISH)
    await message.answer(
        text=menu.title,
        reply_markup=menu.keyboard
    )
    await history_append(state, MenuType.START)
