import uuid
from typing import override, Any
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import Sequence, Row

from src.models.dto.sent_food_response_dto import SentFoodResponseDTO
from src.models.dto.sent_food_request_dto import SentFoodRequestDTO
from src.models.property.detected_food import DetectedFood
from src.models.property.food_statistic import FoodStatistic
from src.models.property.period import Period
from src.services import StatisticService
from src.services.ai_service import AIService
from src.services.db_service import DBService


class FoodService(StatisticService):
    def __init__(self, db_service: DBService, ai_service: AIService):
        super().__init__(db_service)
        self._ai_service = ai_service

    async def sent_food(self, sent_food: SentFoodRequestDTO) -> SentFoodResponseDTO:
        if sent_food.image is None:
            raise HTTPException(status_code=422, detail="Image is null")

        detected_foods = await self._ai_service.scan_image(sent_food.image)
        nutrients = self.get_nutrient_by_name([food.label for food in detected_foods])
        nutrients_by_mass = self.get_food_nutrient_by_mass(detected_foods, nutrients)
        return nutrients_by_mass

    def get_nutrient_by_name(self, food_names: list[str]):
        nutrients: dict[str, FoodStatistic] = {}

        for food_name in food_names:
            row = self._db_service.get_food_by_name(food_name)

            if row is None or row.id is None:
                food_id = str(uuid.uuid4())
                nutrient = self.get_nutrient_from_api(food_name)
                self._db_service.add_food(food_id, nutrient)
            else:
                nutrient = FoodStatistic(**row._mapping)

            nutrients.update({food_name: nutrient})

        return nutrients

    def get_nutrient_from_api(self, food_name: str) -> FoodStatistic:
        pass

    @override
    def _default_dict_value(self):
        return FoodStatistic()

    @override
    def _update_dict_value(self, dict_value: FoodStatistic, new_value: FoodStatistic) -> Any:
        return dict_value.update(new_value)

    @override
    def _get_data_from_db(self, user_id: UUID, period: Period) -> Sequence[Row[Any]]:
        return self._db_service.get_sent_food(user_id, period)

    @override
    def _wrap_func(self, result: dict) -> list[SentFoodResponseDTO]:
        return [
            SentFoodResponseDTO(day=key, statistic=value) for key, value in result
        ]

    @staticmethod
    def get_food_nutrient_by_mass(detected_foods: list[DetectedFood], nutrients: dict[str, FoodStatistic]):
        for food_name in nutrients.keys():
            mass = 0
            for detected_food in detected_foods:
                if food_name == detected_food.label:
                    mass = detected_food.mass
                    break

            nutrients.get(food_name).calculate(mass)

        return nutrients
