from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile

from src.handlers import open_menu_edit_callback
from src.handlers.previous import go_back
from src.models.menu_parts.menu_type import MenuType
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.statistic_type import PeriodType, StatisticType
from src.services.statistic import set_statistic_type, get_statistic_for_period

router = Router()


@router.callback_query(F.data == MenuButtonTitle.STATISTIC.value)
async def statistic_callback(callback: CallbackQuery, state: FSMContext):
    await open_menu_edit_callback(callback, state, MenuType.STATISTIC)
    await callback.answer()

async def statistic_type_handler(callback: CallbackQuery, state: FSMContext, stat_type: StatisticType):
    await set_statistic_type(state, stat_type)
    await open_menu_edit_callback(callback, state, MenuType.PERIOD)
    await callback.answer()

@router.callback_query(F.data == MenuButtonTitle.DRUNK_WATER.value)
async def drunk_water_callback(callback: CallbackQuery, state: FSMContext):
    await statistic_type_handler(callback, state, StatisticType.WATER)

@router.callback_query(F.data == MenuButtonTitle.CALORIE.value)
async def calorie_callback(callback: CallbackQuery, state: FSMContext):
    await statistic_type_handler(callback, state, StatisticType.CALORIE)

async def period_type_handler(callback: CallbackQuery, state: FSMContext, period_type: PeriodType):
    filename = await get_statistic_for_period(state, period_type)
    photo = FSInputFile(filename)
    await callback.message.answer_photo(photo)
    await go_back(callback, state, new_message=True)
    await callback.answer()

@router.callback_query(F.data == MenuButtonTitle.LAST_WEEK.value)
async def last_week_statistic(callback: CallbackQuery, state: FSMContext):
    await period_type_handler(callback, state, PeriodType.WEEK)

@router.callback_query(F.data == MenuButtonTitle.LAST_MONTH.value)
async def last_week_statistic(callback: CallbackQuery, state: FSMContext):
    await period_type_handler(callback, state, PeriodType.MONTH)

@router.callback_query(F.data == MenuButtonTitle.LAST_YEAR.value)
async def last_week_statistic(callback: CallbackQuery, state: FSMContext):
    await period_type_handler(callback, state, PeriodType.YEAR)



