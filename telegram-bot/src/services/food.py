from datetime import date

from aiogram.fsm.context import FSMContext
from aiogram.types import PhotoSize

from src.models.dto.food_response import FoodResponseDTO
from src.models.statistic_type import PeriodType
from src.services import ServerEndpoint, request_post, request_put_image
from src.services.users import get_user_id


async def food_add_request(state: FSMContext, image: PhotoSize):
    # user_id = await get_user_id(state)
    # data = { "user_id": user_id }
    # files = { "file": ("image.jpg", image, "image/jpeg") }
    # resp = await request_put_image(ServerEndpoint.ADD_FOOD, data, files)
    # return resp.json()
    return {
        "day": date.today(),
        "statistic": {
            "name": "Млинці з ягодами",
            "calorie": 340,
            "protein": 8,
            "carbon": 50,
            "fat": 12,
        }
    }

async def food_statistic(user_id: str, period_type: PeriodType, stat_day: date) \
        -> list[FoodResponseDTO]:
    body = { "user_id": user_id, "statistic_date": stat_day.isoformat() }
    url = ServerEndpoint.STATISTIC_FOOD.value.format(stat_type=period_type.value)
    data = (await request_post(url, body)).json()
    return [
        FoodResponseDTO(
            day=item.get('day', date.today().isoformat()),
            name=data.get('name', ''),
            calorie=data.get('calorie', 0),
            protein=data.get('protein', 0.0),
            carbon=data.get('carbon', 0.0),
            fat=data.get('fat', 0.0)
        ) for item in data
    ]

def food_data(result: list[FoodResponseDTO], date_format) -> dict:
    return {
        date.fromisoformat(item.day).strftime(date_format) : item.calorie for item in result
    }