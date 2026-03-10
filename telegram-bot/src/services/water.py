from datetime import date

import httpx

from src.models.dto.water_response import WaterResponseDTO
from src.services import server
from src.models.statistic_type import StatisticType

WATER_API = f"{server()}/api/water"

async def request(method, url, body):
    response = await method(url=url, json=body)
    response.raise_for_status()
    data = response.json()
    return [
        WaterResponseDTO(
            day=item.get('day', date.today()),
            drunk_water=item.get('drunk_water', 0)
        ) for item in data
    ]

async def water_add_request(user_id: str, drunk_water: int) -> WaterResponseDTO:
    async with httpx.AsyncClient() as client:
        body = {
            "user_id": user_id,
            "drunk_water": drunk_water
        }
        data = await request(client.put, f"{WATER_API}/add", body)
        return data[0]

async def water_statistic(user_id: str, period_type: StatisticType, stat_day: date) -> list[WaterResponseDTO]:
    async with httpx.AsyncClient() as client:
        body = {
            "user_id": user_id,
            "statistic_date_str": stat_day.isoformat()
        }
        return await request(client.post, f"{WATER_API}/{period_type.value}", body)

