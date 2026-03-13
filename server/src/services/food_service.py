import os.path
import uuid
from typing import override, Any
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import Sequence, Row

from src.models.dto.sent_food_response_dto import SentFoodResponseDTO
from src.models.dto.sent_food_request_dto import SentFoodRequestDTO
from src.models.property.food_statistic import FoodStatistic
from src.models.property.period import Period
from src.services import StatisticService
from src.services.ai_service import AIService
from src.services.db_service import DBService


class FoodService(StatisticService):
    def __init__(self, db_service: DBService, ai_service: AIService):
        super().__init__(db_service)
        self._ai_service = ai_service

    def sent_food(self, sent_food: SentFoodRequestDTO) -> SentFoodResponseDTO:
        if sent_food.image_path is None:
            raise HTTPException(status_code=400, detail="Image path is null")

        image = self.get_image(sent_food.image_path)
        if sent_food.image_path is None:
            raise HTTPException(status_code=400, detail="Image couldn't be find")

        food_names = self._ai_service.scan_image(image)
        if sent_food.image_path is None:
            raise HTTPException(status_code=400, detail="Image couldn't be scan or interpreter")

        nutrient = self.get_nutrient_by_name(food_names)

        return nutrient

    def get_nutrient_by_name(self, food_names: list[str]):
        nutrients = []

        for food_name in food_names:
            row = self._db_service.get_food_by_name(food_name)

            if row is None or row.user_id is None:
                food_id = str(uuid.uuid4())
                nutrient = self.get_nutrient_from_api(food_name)
                self._db_service.add_food(food_id, nutrient)
            else:
                nutrient = FoodStatistic().from_row(row)

            nutrients.append(nutrient)

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
    def get_image(image_path: str):
        return os.path.abspath(image_path)

