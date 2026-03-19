from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.utils.menu_builder import MenuFactory
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_type import MenuType

router = Router()

async def open_help(message: Message, state: FSMContext):
    menu = await MenuFactory.build_menu(MenuType.HELP, state)

    await message.answer(
        text=menu.title,
        reply_markup=menu.keyboard
    )

@router.message(Command("help"))
async def help_message(message: Message, state: FSMContext):
    await open_help(message, state)

@router.callback_query(F.data == MenuButtonTitle.HELP.value)
async def help_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await open_help(callback.message, state)
