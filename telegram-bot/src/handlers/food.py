from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.handlers import open_menu_edit
from src.models.menu_type import MenuType
from src.models.menu_button_titles import MenuButtonTitle

router = Router()


@router.callback_query(F.data == MenuButtonTitle.FOOD.value)
async def food_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await open_menu_edit(callback, state, MenuType.FOOD)
