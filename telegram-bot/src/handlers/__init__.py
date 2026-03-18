from typing import Union

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.builders.menu_builder import MenuFactory
from src.models.menu_parts.menu_type import MenuType

Event = Union[Message, CallbackQuery]

async def history_append(state: FSMContext, menu_type: MenuType):
    history: list = await state.get_value("menu_history", [])
    if menu_type not in history:
        history.append(menu_type)
        await state.update_data(menu_history=history)

async def history_last(state: FSMContext):
    history: list = await state.get_value("menu_history", [])

    if len(history) <= 1:
        await state.update_data(menu_history=[MenuType.START])
        return MenuType.START

    history.pop()
    last_menu = history[-1]

    await state.update_data(menu_history=history)
    return last_menu

async def open_menu_edit_message(
        message: Message,
        state: FSMContext,
        menu_type: MenuType,
        text: str | None = None,
):
    menu = await MenuFactory.build_menu(menu_type, state)
    await message.answer(
        text=menu.title if text is None else text,
        reply_markup=menu.keyboard
    )
    await history_append(state, menu_type)

async def open_menu_edit_callback(
        callback: CallbackQuery,
        state: FSMContext,
        menu_type: MenuType,
        text: str | None = None,
        new_message: bool = False
):
    menu = await MenuFactory.build_menu(menu_type, state)
    action = callback.message.answer if new_message else callback.message.edit_text
    if new_message:
        await callback.message.delete_reply_markup()
    await action(
        text=menu.title if text is None else text,
        reply_markup=menu.keyboard
    )
    await history_append(state, menu_type)