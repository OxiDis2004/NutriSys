from aiogram.fsm.context import FSMContext
import matplotlib.pyplot as plt
from datetime import date

from src.models.dto.water_response import WaterResponseDTO
from src.models.statistic_type import StatisticType, PeriodType
from src.models.unit import Unit
from src.services.language import translate
from src.services.users import get_user_calorie, get_user_id
from src.services.water import water_statistic


STATISTIC_KEY = 'statistic_type'

async def set_statistic_type(state: FSMContext, stat_type: StatisticType):
    await state.update_data(**{STATISTIC_KEY:stat_type})

async def get_statistic_type(state: FSMContext) -> StatisticType | None:
    stat_type: StatisticType | None = await state.get_value(STATISTIC_KEY, None)
    return StatisticType(stat_type) if stat_type is not None else None

async def get_statistic(state: FSMContext, period_type: PeriodType) -> dict:
    curr_day = date.today()
    stat_type = await get_statistic_type(state)
    user_id = await get_user_id(state)

    match stat_type:
        case StatisticType.CALORIE:
            result = get_user_calorie(state)
            return food_data(result, curr_day)
        case StatisticType.WATER:
            result = await water_statistic(user_id, period_type, curr_day)
            return water_data(period_type, result)

    return {}

def food_data(result, curr_day) -> dict:
    return { curr_day : result }

def water_data(period_type: PeriodType, result: list[WaterResponseDTO]) -> dict:
    match period_type:
        case PeriodType.WEEK:
            return {
                date.fromisoformat(item.day).strftime("%a") : item.drunk_water for item in result
            }

        case PeriodType.MONTH:
            return {
                item.day : item.drunk_water for item in result
            }

        case PeriodType.YEAR:
            return {
                date.fromisoformat(item.day).strftime("%b") : item.drunk_water for item in result
            }

        case _:
            return { item.day : item.drunk_water for item in result }

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
