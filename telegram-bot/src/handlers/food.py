from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.handlers import open_menu_edit_callback
from src.models.menu_parts.menu_type import MenuType
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.services.users import set_user_calorie, get_user_calorie

router = Router()


@router.callback_query(F.data == MenuButtonTitle.FOOD.value)
async def food_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await open_menu_edit_callback(callback, state, MenuType.FOOD)

@router.callback_query(F.data == MenuButtonTitle.ADD_FOOD.value)
async def add_calorie(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    set_user_calorie(callback.from_user.id, 1000)
    total_calorie = get_user_calorie(callback.from_user.id)
    await open_menu_edit_callback(callback, state, MenuType.FOOD, f"Total calorie: {total_calorie} kcal")
