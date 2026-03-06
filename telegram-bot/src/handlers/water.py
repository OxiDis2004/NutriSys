from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.handlers import open_menu_edit
from src.models.menu_title import MenuTitle
from src.models.menu_type import MenuType
from src.models.menu_button_titles import MenuButtonTitle
from src.models.unit import Unit
from src.services.language import translate
from src.services.users import add_water

router = Router()


@router.callback_query(F.data == MenuButtonTitle.WATER.value)
async def water_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await open_menu_edit(callback, state, MenuType.WATER)

def format_answer(telegram_id: int, water: int) -> str:
    translated_text = translate(telegram_id, MenuTitle.DRUNK_TITLE)
    if water >= 1000:
        water = f"{water/1000:.2f}".rstrip("0").rstrip(".")
        translated_unit = translate(telegram_id, Unit.L)
    else:
        translated_unit = translate(telegram_id, Unit.ML)

    return translated_text.format(water=water, unit=translated_unit)

async def add_n_ml(callback: CallbackQuery, state: FSMContext, water: int):
    await callback.answer()
    total_water = add_water(callback.from_user.id, water)
    text = format_answer(callback.from_user.id, total_water)
    await open_menu_edit(callback, state, MenuType.WATER, text)

@router.callback_query(F.data == MenuButtonTitle.ADD_250_ML.value)
async def add_250ml(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await add_n_ml(callback, state, 250)

@router.callback_query(F.data == MenuButtonTitle.ADD_500_ML.value)
async def add_500ml(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await add_n_ml(callback, state, 500)

@router.callback_query(F.data == MenuButtonTitle.ADD_1_L.value)
async def add_1l(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await add_n_ml(callback, state, 1000)

@router.callback_query(F.data == MenuButtonTitle.ADD_1_5_L.value)
async def add_1_5l(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await add_n_ml(callback, state, 1500)
