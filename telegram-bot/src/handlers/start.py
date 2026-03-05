from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.builders.menu_builder import MenuBuilder
from src.handlers import history_append
from src.models.menu_type import MenuType

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    menu = MenuBuilder.build_menu(MenuType.START, message.from_user.id)
    await message.answer(
        text=menu.title,
        reply_markup=menu.keyboard
    )
    await history_append(state, MenuType.START)
