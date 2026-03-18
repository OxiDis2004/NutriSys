from typing import Union

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.handlers import history_last, open_menu_edit_callback, open_menu_edit_message, Event
from src.models.menu_parts.menu_button_titles import MenuButtonTitle

router = Router()


async def go_back(event: Event, state: FSMContext, new_message: bool = False):
    menu = await history_last(state)

    if isinstance(event, CallbackQuery):
        await event.answer()
        await open_menu_edit_callback(
            event,
            state,
            menu,
            new_message=new_message
        )
    else:
        await open_menu_edit_message(event, state, menu)

@router.callback_query(F.data == MenuButtonTitle.BACK.value)
async def previous_callback(callback: CallbackQuery, state: FSMContext, new_message: bool = False):
    await go_back(callback, state, new_message)