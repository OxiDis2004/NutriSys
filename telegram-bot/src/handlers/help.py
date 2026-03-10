from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from src.builders.menu_builder import MenuBuilder
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_type import MenuType

router = Router()

async def open_help(message: Message, telegram_id: int):
    menu = MenuBuilder.build_menu(MenuType.HELP, telegram_id)

    await message.answer(
        text=menu.title,
        reply_markup=menu.keyboard
    )

@router.message(Command("help"))
async def help_message(message: Message):
    await open_help(message, message.from_user.id)

@router.callback_query(F.data == MenuButtonTitle.HELP.value)
async def help_callback(callback: CallbackQuery):
    await callback.answer()
    await open_help(callback.message, callback.from_user.id)
