import uuid
from io import BytesIO

import pytest
from fastapi import HTTPException, UploadFile

from src.models.dto.food_record_request_dto import FoodRecordRequestDTO
from src.models.property.food_statistic import FoodStatistic
from src.services.food_service import FoodService


class TestFoodService:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mocker):
        self.db_service_mock = mocker.Mock()
        self.ai_service_mock = mocker.AsyncMock()

        self.food_service = FoodService(
            self.db_service_mock,
            self.ai_service_mock,
        )

        self.image_mock = UploadFile(
            filename="test.jpg",
            file=BytesIO(b"fake image bytes"),
        )

    @pytest.mark.asyncio
    async def test_add_food_record_successful(self, mocker):
        request = FoodRecordRequestDTO(
            user_id=uuid.uuid4(),
            image=self.image_mock
        )

        detected_food_names = ["apple", "banana"]

        apple = mocker.Mock()
        apple.name = "apple"
        apple.mass = 150
        apple.calories = 52
        apple.proteins = 0.3
        apple.fats = 0.2
        apple.carbohydrates = 14

        banana = mocker.Mock()
        banana.name = "banana"
        banana.mass = 120
        banana.calories = 89
        banana.proteins = 1.1
        banana.fats = 0.3
        banana.carbohydrates = 23

        self.ai_service_mock.scan_image.return_value = detected_food_names

        mocker.patch.object(
            self.food_service,
            "get_food_information",
            return_value=[apple, banana],
        )

        mocker.patch.object(
            self.food_service,
            "get_foods_response",
            return_value=["response_1", "response_2"],
        )

        result = await self.food_service.add_food_record(request)

        assert result == ["response_1", "response_2"]
        self.ai_service_mock.scan_image.assert_called_once_with(self.image_mock)
        self.food_service.get_food_information.assert_called_once_with(detected_food_names)
        self.food_service.get_foods_response.assert_called_once_with([apple, banana])

    @pytest.mark.asyncio
    async def test_add_food_record_failed_when_image_is_none(self):
        request = FoodRecordRequestDTO(
            user_id=uuid.uuid4(),
            image=None
        )

        with pytest.raises(HTTPException) as e_info:
            await self.food_service.add_food_record(request)

        assert e_info.value.status_code == 422
        assert e_info.value.detail == "Image is null"

        self.ai_service_mock.scan_image.assert_not_called()

    def test_get_food_information_when_foods_exist_in_db(self, mocker):
        food_names = ["apple", "banana"]

        apple = mocker.Mock()
        apple.name = "apple"

        banana = mocker.Mock()
        banana.name = "banana"

        self.db_service_mock.get_foods_by_names.return_value = [
            apple,
            banana,
        ]

        result = self.food_service.get_food_information(food_names)

        assert len(result) == 2
        self.db_service_mock.get_foods_by_names.assert_called_once_with(food_names)
        self.db_service_mock.add_food.assert_not_called()

    def test_get_food_information_when_food_not_found_in_db(self, mocker):
        food_names = ["apple"]

        self.db_service_mock.get_foods_by_names.return_value = []

        food_from_api = {
            "name": "apple",
            "mass": 100,
            "calories": 52,
            "proteins": 0.3,
            "fats": 0.2,
            "carbohydrates": 14,
        }

        mocker.patch.object(
            self.food_service,
            "get_nutrient_from_api",
            return_value=food_from_api,
        )

        result = self.food_service.get_food_information(food_names)

        assert len(result) == 1
        self.db_service_mock.get_foods_by_names.assert_called_once_with(food_names)
        self.food_service.get_nutrient_from_api.assert_called_once_with("apple")
        self.db_service_mock.add_food.assert_called_once()

    def test_default_dict_value(self):
        result = self.food_service._default_dict_value()

        assert isinstance(result, FoodStatistic)

    def test_get_data_from_db(self, mocker):
        user_id = uuid.uuid4()
        period = mocker.Mock()

        self.db_service_mock.get_sent_food.return_value = ["food_1", "food_2"]

        result = self.food_service._get_data_from_db(user_id, period)

        assert result == ["food_1", "food_2"]
        self.db_service_mock.get_sent_food.assert_called_once_with(user_id, period)
