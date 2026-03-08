from aiogram.fsm.context import FSMContext
import matplotlib.pyplot as plt
from datetime import date, timedelta

from src.models.menu_button_titles import MenuButtonTitle
from src.models.statistic_type import StatisticType
from src.models.unit import Unit
from src.services.language import translate
from src.services.users import get_user_water, get_user_calorie


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

    from_statistic = get_user_water if stat_type is StatisticType.WATER else get_user_calorie

    data = {}
    for i in range(7):
        next_day = (curr_day - timedelta(days=i)).strftime("%Y-%m-%d")
        value = from_statistic(telegram_id, next_day)
        data.update({ next_day: value })

    return data

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
