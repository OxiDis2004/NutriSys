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

STATISTIC_MAP = {
    MenuButtonTitle.DRUNK_WATER.value: StatisticType.WATER,
    MenuButtonTitle.CALORIE.value: StatisticType.CALORIE
}

PERIOD_MAP = {
    MenuButtonTitle.LAST_WEEK.value: PeriodType.WEEK,
    MenuButtonTitle.LAST_MONTH.value: PeriodType.MONTH,
    MenuButtonTitle.LAST_YEAR.value: PeriodType.YEAR,
}

@router.callback_query(F.data == MenuButtonTitle.STATISTIC.value)
async def statistic_callback(callback: CallbackQuery, state: FSMContext):
    await open_menu_edit_callback(callback, state, MenuType.STATISTIC)
    await callback.answer()

@router.callback_query(F.data.in_(STATISTIC_MAP.keys()))
async def statistic_type_handler(callback: CallbackQuery, state: FSMContext):
    await set_statistic_type(state, STATISTIC_MAP[callback.data])
    await open_menu_edit_callback(callback, state, MenuType.PERIOD)
    await callback.answer()

@router.callback_query(F.data.in_(PERIOD_MAP.keys()))
async def period_type_handler(callback: CallbackQuery, state: FSMContext):
    filename = await get_statistic_for_period(state, PERIOD_MAP[callback.data])
    photo = FSInputFile(filename)
    await callback.message.answer_photo(photo)
    await go_back(callback, state, new_message=True)
    await callback.answer()



