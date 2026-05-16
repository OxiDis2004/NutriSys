import datetime
import uuid
from typing import Any, override
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import Row, Sequence

from src.models.dto.food_record_request_dto import FoodRecordRequestDTO
from src.models.dto.food_record_response_dto import FoodRecordResponseDTO
from src.models.entity.food import Food
from src.models.property.food_statistic import FoodStatistic
from src.models.property.period import Period
from src.services import StatisticService
from src.services.ai_service import AIService
from src.services.db_service import DBService


class FoodService(StatisticService):
    """Service responsible for food-related business logic.

    Provides methods for managing food entries, calculating nutritional
    statistics, processing calorie information and aggregating user food data.

    Inherits:
        StatisticService: Base service for statistical calculations.

    Responsibilities:
        - Create and manage food records
        - Calculate calorie and nutrient statistics
        - Aggregate food consumption history
        - Provide food-related analytics for users
    """

    def __init__(self, db_service: DBService, ai_service: AIService):
        super().__init__(db_service)
        self._ai_service = ai_service

    async def add_food_record(self, sent_food: FoodRecordRequestDTO) -> list[FoodRecordResponseDTO]:
        """Process a sent food image and calculate nutrition values.

        Args:
            sent_food (FoodRecordRequestDTO): Request containing the food image.

        Returns:
            FoodRecordResponseDTO: Calculated food nutrition response.

        Raises:
            HTTPException: If the image is missing.
        """

        if sent_food.image is None:
            raise HTTPException(status_code=422, detail="Image is null")

        detected_food_names = await self._ai_service.scan_image(sent_food.image)
        foods_information = self.get_food_information(detected_food_names)
        foods_response = self.get_foods_response(foods_information)
        return foods_response

    def get_food_information(self, food_names: list[str]) -> list[Food]:
        """Return nutrient information for food names.

        Loads nutrient data from the database when available. If food data is not
        found, it is requested from an external API and saved to the database.

        Args:
            food_names (list[str]): Recognized food names.

        Returns:
            dict[str, FoodStatistic]: Nutrient values indexed by food name.
        """

        result: list[Food] = []

        found_foods = {
            found_food.name: found_food
            for found_food in self._db_service.get_foods_by_names(food_names)
        }

        for food_name in food_names:
            if food_name not in found_foods:
                food_id = str(uuid.uuid4())
                food = self.get_nutrient_from_api(food_name)
                self._db_service.add_food(food_id, food)
                found_foods[food_name] = food

            result.append(Food(**found_foods[food_name]))

        return result

    def get_nutrient_from_api(self, food_name: str) -> Food:
        """Load nutrient information from an external API.

        Args:
            food_name (str): Food name.

        Returns:
            FoodStatistic: Nutrient information for the requested food.
        """
        pass

    @override
    def _default_dict_value(self):
        return FoodStatistic()

    @override
    def _update_dict_value(
            self, dict_value: FoodStatistic, new_value: FoodStatistic
    ) -> Any:
        return dict_value.update(new_value)

    @override
    def _get_data_from_db(self, user_id: UUID, period: Period) -> Sequence[Row[Any]]:
        return self._db_service.get_sent_food(user_id, period)

    @override
    def _wrap_func(self, result: dict) -> list[FoodRecordResponseDTO]:
        return [FoodRecordResponseDTO(day=key, statistic=value) for key, value in result]

    @staticmethod
    def get_foods_response(
            detected_foods: list[Food]
    ) -> list[FoodRecordResponseDTO]:
        """Calculate nutrient values according to detected food mass.

        Args:
            detected_foods (list[Food]): Foods detected by the AI model and with own information.

        Returns:
            list[FoodRecordResponseDTO]: Nutrient data recalculated by mass.
        """
        result: list[FoodRecordResponseDTO] = []

        for food in detected_foods:
            calculated_by_mass_food: FoodStatistic = FoodStatistic(**food.__dict__).calculate(
                food.mass
            )
            result.append(
                FoodRecordResponseDTO(
                    day=datetime.datetime.now(), statistic=calculated_by_mass_food
                )
            )

        return result
