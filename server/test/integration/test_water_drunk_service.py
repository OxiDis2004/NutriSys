import datetime
import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy.engine.create import create_engine

from src.models.dto.water_request_dto import WaterRequestDTO
from src.models.dto.water_statistic_request_dto import WaterStatisticRequestDTO
from src.services.db_service import DBService
from src.services.water_service import WaterService


class TestWaterDrunkService:
    @pytest.fixture(scope="function", autouse=True)
    def setup_service(self):
        self.engine_mock = create_engine(
            f"sqlite:///:memory:",
            connect_args={"check_same_thread": False},
        )
        self.db_service = DBService(self.engine_mock)
        self.water_service = WaterService(self.db_service)
        self.user_id = str(uuid.uuid4())

        yield

        self.engine_mock = None
        self.db_service = None
        self.water_service = None

    def test_failed_add_water(self):
        with pytest.raises(Exception) as e_info:
            self.water_service.add_drunk_water(WaterRequestDTO(user_id=None, drunk_water=250))

        assert e_info.errisinstance(HTTPException)
        assert e_info.value.status_code == 400
        assert e_info.value.detail == "User id is null"

    def test_add_water(self):
        drunk = self.water_service.add_drunk_water(WaterRequestDTO(user_id=self.user_id, drunk_water=250))
        assert drunk.drunk_water_day == 250

    def test_add_water_3_times(self):
        request_1 = WaterRequestDTO(user_id=self.user_id, drunk_water=500)
        drunk = self.water_service.add_drunk_water(request_1)
        assert drunk.drunk_water_day == request_1.drunk_water

        request_2 = WaterRequestDTO(user_id=self.user_id, drunk_water=250)
        drunk = self.water_service.add_drunk_water(request_2)
        assert drunk.drunk_water_day == request_1.drunk_water + request_2.drunk_water

        request_3 = WaterRequestDTO(user_id=self.user_id, drunk_water=1000)
        drunk = self.water_service.add_drunk_water(request_3)
        assert (drunk.drunk_water_day == request_1.drunk_water + request_2.drunk_water +
                request_3.drunk_water)

    @pytest.fixture
    def initialize_2000(self):
        self.water_service.add_drunk_water(WaterRequestDTO(user_id=self.user_id, drunk_water=500))
        self.water_service.add_drunk_water(WaterRequestDTO(user_id=self.user_id, drunk_water=1000))
        self.water_service.add_drunk_water(WaterRequestDTO(user_id=self.user_id, drunk_water=500))

    def test_get_drunk_water(self, initialize_2000):
        water = self.water_service.statistic(
            WaterStatisticRequestDTO(
                user_id=self.user_id,
                day=datetime.date.today()
            )
        )

        assert len(water) == 1
        assert water[datetime.date.today().isoformat()] == 2000
