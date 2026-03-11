import importlib
from random import randint
from datetime import date, datetime, timedelta
from uuid import uuid4

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine

from src.dependencies import get_db_service
from src.models.dto.user_dto import UserDTO

language_en = (2, "en")
user: UserDTO = UserDTO(id=uuid4(), telegram_id=759786972, language=language_en[1])

@pytest.mark.asyncio
class TestWaterEndpoints:

    @pytest.fixture
    def setup_mocks(self, mocker):
        self.engine_mock = create_engine(
            f"sqlite:///:memory:",
            connect_args={"check_same_thread": False},
        )
        mocker.patch("src.dependencies.create_db_engine", return_value=self.engine_mock)

        import src.main
        importlib.reload(src.main)
        from src.main import create_app
        self.app = create_app()

        yield

        self.app = None
        get_db_service().close_session()

    @pytest.fixture
    def initialize_language(self, setup_mocks):
        get_db_service()._add_language(language_en[1])

    @pytest.fixture
    def initialize_user(self, setup_mocks):
        get_db_service().add_user(user, datetime.today())

    async def _water_add_to_user(self, water: int):
        async with (
            AsyncClient(
                transport=ASGITransport(app=self.app),
                base_url="http://test"
            ) as client
        ):
            resp = await client.put(
                "/api/water/add",
                json={ "user_id": str(user.id), "drunk_water": water }
            )

        assert resp.status_code == 200
        return resp.json()

    async def test_water_add(self, initialize_language, initialize_user):
        data = await self._water_add_to_user(500)
        assert data["day"] == date.today().isoformat()
        assert data["drunk_water"] == 500

    async def test_water_add_2_times(self, initialize_language, initialize_user):
        data = await self._water_add_to_user(1000)
        assert data["day"] == date.today().isoformat()
        assert data["drunk_water"] == 1000

        data = await self._water_add_to_user(1000)
        assert data["day"] == date.today().isoformat()
        assert data["drunk_water"] == 2000

    @pytest.fixture
    def add_water_to_user(self, setup_mocks):
        curr_day = date.today()
        water_ml = [250, 500, 1000, 1500]

        for i in range(7):
            get_db_service().add_drunk_water(user.id, water_ml[randint(0,3)], curr_day)
            curr_day -= timedelta(days=1)

    async def water_statistic(self, _type):
        async with (
            AsyncClient(
                transport=ASGITransport(app=self.app),
                base_url="http://test"
            ) as client
        ):
            resp = await client.post(
                url=f"/api/water/statistic/{_type}",
                json={ "user_id": str(user.id), "statistic_date": date.today().isoformat() }
            )

        assert resp.status_code == 200
        return resp.json()

    async def test_water_stat_day(self, initialize_language, initialize_user, add_water_to_user):
        data = await self.water_statistic("day")
        assert len(data) == 1

    async def test_water_stat_week(self, initialize_language, initialize_user, add_water_to_user):
        data = await self.water_statistic("week")
        assert len(data) == 7

    async def test_water_stat_month(self, initialize_language, initialize_user, add_water_to_user):
        data = await self.water_statistic("month")
        assert len(data) == 28 or len(data) == 30 or len(data) == 31

    async def test_water_stat_year(self, initialize_language, initialize_user, add_water_to_user):
        data = await self.water_statistic("year")
        assert len(data) == 12