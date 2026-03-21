from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.handlers import open_menu_edit_callback
from src.models.menu_parts.menu_title import MenuTitle
from src.models.menu_parts.menu_type import MenuType
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.unit import Unit
from src.utils import translate
from src.services.water import water_add_request

router = Router()

WATER_ADD_MAP = {
    MenuButtonTitle.ADD_250_ML.value: 250,
    MenuButtonTitle.ADD_500_ML.value: 500,
    MenuButtonTitle.ADD_1_L.value: 1000,
    MenuButtonTitle.ADD_1_5_L.value: 1500
}

@router.callback_query(F.data == MenuButtonTitle.WATER.value)
async def water_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await open_menu_edit_callback(callback, state, MenuType.WATER)

async def format_answer(state: FSMContext, water: int) -> str:
    if water >= 1000:
        water = f"{water/1000:.2f}".rstrip("0").rstrip(".")
        translated_unit = await translate(state, Unit.L)
    else:
        translated_unit = await translate(state, Unit.ML)

    translated_text = await translate(state, MenuTitle.DRUNK)
    return translated_text.format(water=water, unit=translated_unit)

@router.callback_query(F.data.in_(WATER_ADD_MAP.keys()))
async def add_n_ml(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    total_water = await water_add_request(state, WATER_ADD_MAP[callback.data])
    text = await format_answer(state, total_water.drunk_water)
    await open_menu_edit_callback(callback, state, MenuType.WATER, text)