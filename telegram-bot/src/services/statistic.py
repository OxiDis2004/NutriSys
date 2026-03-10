from aiogram.fsm.context import FSMContext
import matplotlib.pyplot as plt
from datetime import date

from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.statistic_type import StatisticType
from src.models.unit import Unit
from src.models.user import User
from src.services.language import translate
from src.services.users import get_user_calorie, get_current_user
from src.services.water import water_statistic


async def set_statistic_type(state: FSMContext, _type: MenuButtonTitle):
    stat_type = ''

    match _type:
        case MenuButtonTitle.DRUNK_WATER: stat_type = StatisticType.WATER
        case MenuButtonTitle.CALORIE: stat_type = StatisticType.CALORIE
        case _: raise Exception("Wrong statistic type")

    await state.update_data(statistic_type=stat_type.value)

async def get_statistic_type(state: FSMContext) -> StatisticType | None:
    _type: StatisticType | None = await state.get_value('statistic_type', None)

    if _type is None:
        return None

    return StatisticType(_type)

def get_period_type(tmp_period_type: MenuButtonTitle) -> StatisticType | None:
    period_type = None

    match tmp_period_type:
        case MenuButtonTitle.LAST_WEEK: period_type = StatisticType.WEEK
        case MenuButtonTitle.LAST_MONTH: period_type = StatisticType.MONTH
        case MenuButtonTitle.LAST_YEAR: period_type = StatisticType.YEAR

    return period_type

async def get_statistic(telegram_id: int, stat_type: StatisticType, period_type: StatisticType) -> dict:
    curr_day = date.today()
    user: User = get_current_user(telegram_id)

    match stat_type:
        case StatisticType.CALORIE:
            result = get_user_calorie(telegram_id, curr_day.strftime("%Y-%m-%d"))
            return food_data(result, curr_day)
        case StatisticType.WATER:
            result = await water_statistic(user.user_id, period_type, curr_day)
            return water_data(result)

    return {}

def food_data(result, curr_day) -> dict:
    return { curr_day : result }

def water_data(result) -> dict:
    return { item.day.strftime("%Y-%m-%d") : item.drunk_water for item in result }

async def generate_chart(
        telegram_id: int,
        stat_type: StatisticType,
        period_type: StatisticType,
        data: dict
):
    x = [k for k in data.keys()]
    y = [v for v in data.values()]

    plt.figure()
    plt.bar(x, y)

    plt.title(translate(telegram_id, stat_type))
    plt.xlabel(translate(telegram_id, period_type))
    plt.ylabel(translate(telegram_id, Unit.L))

    file = f"chart_{telegram_id}_{stat_type.value}_{period_type.value}.png"
    plt.savefig(file)
    plt.close()

    return file

async def get_statistic_for_period(
        telegram_id: int,
        state: FSMContext,
        period_type: MenuButtonTitle
):
    stat_type = await get_statistic_type(state)
    period_type = get_period_type(period_type)

    data = await get_statistic(telegram_id, stat_type, period_type)
    filename = await generate_chart(telegram_id, stat_type, period_type, data)

    return filename
