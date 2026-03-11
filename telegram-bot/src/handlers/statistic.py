from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile

from src.handlers import open_menu_edit
from src.handlers.previous import previous_callback
from src.models.menu_parts.menu_type import MenuType
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.services.language import translate
from src.services.statistic import set_statistic_type, get_statistic_for_period

router = Router()


@router.callback_query(F.data == MenuButtonTitle.STATISTIC.value)
async def statistic_callback(callback: CallbackQuery, state: FSMContext):
    await open_menu_edit(callback, state, MenuType.STATISTIC)
    await callback.answer()

async def statistic_type_handler(callback: CallbackQuery, state: FSMContext, _type: MenuButtonTitle):
    await set_statistic_type(state, _type)
    await open_menu_edit(callback, state, MenuType.PERIOD)
    await callback.answer()

@router.callback_query(F.data == MenuButtonTitle.DRUNK_WATER.value)
async def drunk_water_callback(callback: CallbackQuery, state: FSMContext):
    await statistic_type_handler(callback, state, MenuButtonTitle.DRUNK_WATER)

@router.callback_query(F.data == MenuButtonTitle.CALORIE.value)
async def calorie_callback(callback: CallbackQuery, state: FSMContext):
    await statistic_type_handler(callback, state, MenuButtonTitle.CALORIE)

async def period_type_handler(callback: CallbackQuery, state: FSMContext, period_type: MenuButtonTitle):
    filename = await get_statistic_for_period(callback.from_user.id, state, period_type)
    photo = FSInputFile(filename)
    await callback.message.answer_photo(photo)
    await previous_callback(callback, state, new_message=True)
    await callback.answer()

@router.callback_query(F.data == MenuButtonTitle.LAST_WEEK.value)
async def last_week_statistic(callback: CallbackQuery, state: FSMContext):
    await period_type_handler(callback, state, MenuButtonTitle.LAST_WEEK)

@router.callback_query(F.data == MenuButtonTitle.LAST_MONTH.value)
async def last_week_statistic(callback: CallbackQuery, state: FSMContext):
    await period_type_handler(callback, state, MenuButtonTitle.LAST_MONTH)

@router.callback_query(F.data == MenuButtonTitle.LAST_YEAR.value)
async def last_week_statistic(callback: CallbackQuery, state: FSMContext):
    await period_type_handler(callback, state, MenuButtonTitle.LAST_YEAR)



