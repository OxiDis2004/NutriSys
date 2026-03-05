from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.builders.menu_builder import MenuBuilder
from src.models.menu_type import MenuType


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
        callback: CallbackQuery,
        state: FSMContext,
        menu_type: MenuType,
        text: str | None = None
):
    menu = MenuBuilder.build_menu(menu_type, callback.from_user.id)
    await callback.message.edit_text(
        text=menu.title if text is None else text,
        reply_markup=menu.keyboard
    )
    await history_append(state, menu_type)