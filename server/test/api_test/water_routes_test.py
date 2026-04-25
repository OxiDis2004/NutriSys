from datetime import date, timedelta
from random import randint

import pytest
from httpx import ASGITransport, AsyncClient

from src.dependencies import get_services
from test import USER
from test.api_test import BaseTestEndpoint


@pytest.mark.asyncio
class TestWaterEndpoints(BaseTestEndpoint):
    async def _water_add_to_user(self, water: int):
        async with AsyncClient(
                transport=ASGITransport(app=self.app), base_url="http://test"
        ) as client:
            resp = await client.put(
                "/api/water/add", json={ "user_id": USER.user_id, "drunk_water": water }
            )

        assert resp.status_code == 200
        return resp.json()

    async def water_test(self, add: int, expected: int):
        data = await self._water_add_to_user(add)
        assert data["day"] == date.today().isoformat()
        assert data["drunk_water"] == expected

    async def test_water_add(self, initialize_user):
        await self.water_test(500, 500)

    async def test_water_add_2_times(self, initialize_user):
        await self.water_test(1000, 1000)
        await self.water_test(1000, 2000)

    @pytest.fixture
    def add_water_to_user(self, setup_app):
        curr_day = date.today()
        water_ml = [250, 500, 1000, 1500]

        for _ in range(7):
            get_services().db_service.add_drunk_water(
                USER.user_id, water_ml[randint(0, 3)], curr_day
            )
            curr_day -= timedelta(days=1)

    async def water_statistic(self, _type):
        async with AsyncClient(
                transport=ASGITransport(app=self.app), base_url="http://test"
        ) as client:
            resp = await client.post(
                url=f"/api/water/statistic/{_type}",
                json={
                    "user_id": USER.user_id,
                    "statistic_date": date.today().isoformat(),
                },
            )

        assert resp.status_code == 200
        return resp.json()

    async def test_water_stat_day(self, initialize_user, add_water_to_user):
        data = await self.water_statistic("day")
        assert len(data) == 1

    async def test_water_stat_week(self, initialize_user, add_water_to_user):
        data = await self.water_statistic("week")
        assert len(data) == 7

    async def test_water_stat_month(self, initialize_user, add_water_to_user):
        data = await self.water_statistic("month")
        assert len(data) == 28 or len(data) == 30 or len(data) == 31

    async def test_water_stat_year(self, initialize_user, add_water_to_user):
        data = await self.water_statistic("year")
        assert len(data) == 12
