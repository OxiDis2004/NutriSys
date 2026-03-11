from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.builders.menu_builder import MenuBuilder
from src.handlers import history_last, open_menu_edit
from src.menus.base_menu import BaseMenu
from src.models.menu_parts.menu_button_titles import MenuButtonTitle

router = Router()


@router.callback_query(F.data == MenuButtonTitle.BACK.value)
async def previous_callback(callback: CallbackQuery, state: FSMContext, new_message: bool = False):
    await callback.answer()
    menu = await history_last(state)
    await open_menu_edit(callback, state, menu, new_message=new_message)
