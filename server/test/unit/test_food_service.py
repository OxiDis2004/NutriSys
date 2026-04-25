import pytest

from src.services.food_service import FoodService


class TestFoodService:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mocker):
        self.db_service_mock = mocker.Mock()
        self.ai_service_mock = mocker.Mock()
        self.food_service = FoodService(self.db_service_mock, self.ai_service_mock)

    def test_sent_food(self):
        pass
