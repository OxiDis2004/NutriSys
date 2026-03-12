from datetime import date

from src.models.dto.water_response import WaterResponseDTO
from src.services import request_put, request_post
from src.models.statistic_type import StatisticType

async def water_add_request(user_id: str, drunk_water: int) -> WaterResponseDTO:
    body = {
        "user_id": user_id,
        "drunk_water": drunk_water
    }
    data = (await request_put(f"/water/add", body)).json()
    return WaterResponseDTO(
        day=data.get('day', date.today()),
        drunk_water=data.get('drunk_water', 0)
    )

async def water_statistic(user_id: str, period_type: StatisticType, stat_day: date) -> list[WaterResponseDTO]:
    body = {
        "user_id": user_id,
        "statistic_date": stat_day.isoformat()
    }
    data = (await request_post(f"/water/{period_type.value}", body)).json()
    return [
        WaterResponseDTO(
            day=item.get('day', date.today().isoformat()),
            drunk_water=item.get('drunk_water', 0)
        ) for item in data
    ]
