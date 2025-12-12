import os.path
import uuid

from fastapi import HTTPException

from src.models.dto.nutrient_food_dto import NutrientFoodDTO
from src.models.dto.sent_food_dto import SentFoodDTO
from src.models.dto.statistic_request_dto import StatisticRequestDTO
from src.models.dto.statistic_response_dto import StatisticResponseDTO
from src.services.ai_service import AIService
from src.services.db_service import DBService


class FoodService:
    def __init__(self, db_service: DBService, ai_service: AIService):
        self._db_service = db_service
        self._ai_service = ai_service

    def sent_food(self, sent_food: SentFoodDTO) -> NutrientFoodDTO:
        if sent_food.image_path is None:
            raise HTTPException(status_code=400, detail="Image path is null")

        image = self.get_image(sent_food.image_path)
        if sent_food.image_path is None:
            raise HTTPException(status_code=400, detail="Image couldn't be find")

        food_name = self._ai_service.scan_image(image)
        if sent_food.image_path is None:
            raise HTTPException(status_code=400, detail="Image couldn't be scan or interpreter")

        nutrient = self.get_nutrient_by_name(food_name)

        return nutrient

    def get_nutrient_by_name(self, food_name: str):
        row = self._db_service.get_food(food_name)

        if row is None or row.id is None:
            id = str(uuid.uuid4())
            nutrient = self.get_nutrient_from_api(food_name)
            self._db_service.add_food(id, nutrient)
        else:
            nutrient = NutrientFoodDTO(
                name=row.name,
                calorie=row.calory,
                protein=row.protein,
                carbon=row.carbon,
                fat=row.fat
            )

        return nutrient

    def get_nutrient_from_api(self, food_name: str) -> NutrientFoodDTO:
        pass

    def statistic(self, request_dto: StatisticRequestDTO) -> StatisticResponseDTO:
        pass

    @staticmethod
    def get_image(image_path: str):
        return os.path.abspath(image_path)

