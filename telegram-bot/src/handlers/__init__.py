from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.builders.menu_builder import MenuBuilder
from src.models.menu_parts.menu_type import MenuType


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

async def open_menu_edit(
        message: Message,
        user_id: int,
        state: FSMContext,
        menu_type: MenuType,
        text: str | None = None,
        new_message: bool = False
):
    menu = MenuBuilder.build_menu(menu_type, user_id)
    action = message.answer if new_message else message.edit_text
    if new_message:
        await message.delete_reply_markup()
    await action(
        text=menu.title if text is None else text,
        reply_markup=menu.keyboard
    )
    await history_append(state, menu_type)

async def open_menu_edit_message(
        message: Message,
        state: FSMContext,
        menu_type: MenuType,
        text: str | None = None,
        new_message: bool = False
):
    await open_menu_edit(
        message,
        message.from_user.id,
        state,
        menu_type,
        text,
        new_message
    )

async def open_menu_edit_callback(
        callback: CallbackQuery,
        state: FSMContext,
        menu_type: MenuType,
        text: str | None = None,
        new_message: bool = False
):
    await open_menu_edit(
        callback.message,
        callback.from_user.id,
        state,
        menu_type,
        text,
        new_message
    )