from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.builders.menu_builder import MenuBuilder
from src.handlers import history_last
from src.menus.base_menu import BaseMenu
from src.models.menu_parts.menu_button_titles import MenuButtonTitle

router = Router()


@router.callback_query(F.data == MenuButtonTitle.BACK.value)
async def previous_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    menu = await get_last_menu(state, callback.from_user.id)
    await callback.message.edit_text(
        text=menu.title,
        reply_markup=menu.keyboard
    )

async def get_last_menu(state: FSMContext, telegram_id: int) -> BaseMenu:
    last_menu = await history_last(state)
    return MenuBuilder.build_menu(last_menu, telegram_id)
