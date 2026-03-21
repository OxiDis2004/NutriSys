from aiogram.fsm.context import FSMContext
import matplotlib.pyplot as plt
from datetime import date

from src.models.fsm_keys import FSMKeys
from src.models.statistic_type import StatisticType, PeriodType
from src.models.unit import Unit
from src.services.food import food_data, food_statistic
from src.utils import translate
from src.services.users import get_user_id
from src.services.water import water_statistic, water_data

async def set_statistic_type(state: FSMContext, stat_type: StatisticType):
    await state.update_data(**{ FSMKeys.STATISTIC_KEY.value:stat_type })

async def get_statistic_type(state: FSMContext) -> StatisticType | None:
    stat_type: StatisticType | None = await state.get_value(FSMKeys.STATISTIC_KEY.value, None)
    return StatisticType(stat_type) if stat_type is not None else None

def get_date_format(period_type: PeriodType):
    date_format = "%a"

    match period_type:
        case PeriodType.DAY: date_format = "%a"
        case PeriodType.WEEK: date_format = "%a"
        case PeriodType.MONTH: date_format = "%d"
        case PeriodType.YEAR: date_format = "%b"

    return date_format

async def get_statistic(state: FSMContext, period_type: PeriodType) -> dict:
    curr_day = date.today()
    stat_type = await get_statistic_type(state)
    user_id = await get_user_id(state)
    date_format = get_date_format(period_type)

    match stat_type:
        case StatisticType.CALORIE:
            result = await food_statistic(user_id, period_type, curr_day)
            return food_data(result, date_format)
        case StatisticType.WATER:
            result = await water_statistic(user_id, period_type, curr_day)
            return water_data(result, date_format)

    return {}

async def generate_chart(
        state: FSMContext,
        stat_type: StatisticType,
        period_type: PeriodType,
        data: dict
):
    x = [k for k in data.keys()]
    y = [v for v in data.values()]

    plt.figure()
    plt.bar(x, y)

    user_id = await get_user_id(state)
    plt.title(await translate(state, stat_type))
    plt.xlabel(await translate(state, period_type))
    plt.ylabel(await translate(state, Unit.ML))

    file = f"chart_{user_id}_{stat_type.value}_{period_type.value.split('/')[1]}.png"
    plt.savefig(file)
    plt.close()

    return file

async def get_statistic_for_period(
        state: FSMContext,
        period_type: PeriodType
):
    stat_type = await get_statistic_type(state)
    data = await get_statistic(state, period_type)
    return await generate_chart(state, stat_type, period_type, data)
