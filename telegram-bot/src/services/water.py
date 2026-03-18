from datetime import date

from aiogram.fsm.context import FSMContext

from src.models.dto.water_response import WaterResponseDTO
from src.services import request_put, request_post, ServerEndpoint
from src.models.statistic_type import PeriodType
from src.services.users import get_user_id


async def water_add_request(state: FSMContext, drunk_water: int) -> WaterResponseDTO:
    user_id = await get_user_id(state)
    body = { "user_id": user_id, "drunk_water": drunk_water }
    data = (await request_put(ServerEndpoint.ADD_WATER.value, body)).json()
    return WaterResponseDTO(
        day=data.get('day', date.today()),
        drunk_water=data.get('drunk_water', 0)
    )

async def water_statistic(user_id: str, period_type: PeriodType, stat_day: date) \
        -> list[WaterResponseDTO]:
    body = { "user_id": user_id, "statistic_date": stat_day.isoformat() }
    url = ServerEndpoint.STATISTIC_WATER.value.format(stat_type=period_type.value)
    data = (await request_post(url, body)).json()
    return [
        WaterResponseDTO(
            day=item.get('day', date.today().isoformat()),
            drunk_water=item.get('drunk_water', 0)
        ) for item in data
    ]
