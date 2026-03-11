from datetime import date

import httpx

from src.models.dto.water_response import WaterResponseDTO
from src.services import server, request
from src.models.statistic_type import StatisticType

WATER_API = f"{server()}/api/water"

async def water_request(method, url, body):
    return (await request(method, url, body)).json()

async def water_add_request(user_id: str, drunk_water: int) -> WaterResponseDTO:
    async with httpx.AsyncClient() as client:
        body = {
            "user_id": user_id,
            "drunk_water": drunk_water
        }
        data = await water_request(client.put, f"{WATER_API}/add", body)
        return WaterResponseDTO(
            day=data.get('day', date.today()),
            drunk_water=data.get('drunk_water', 0)
        )

async def water_statistic(user_id: str, period_type: StatisticType, stat_day: date) -> list[WaterResponseDTO]:
    async with httpx.AsyncClient() as client:
        body = {
            "user_id": user_id,
            "statistic_date": stat_day.isoformat()
        }
        data = await water_request(client.post, f"{WATER_API}/{period_type.value}", body)
        return [
            WaterResponseDTO(
                day=item.get('day', date.today().isoformat()),
                drunk_water=item.get('drunk_water', 0)
            ) for item in data
        ]
