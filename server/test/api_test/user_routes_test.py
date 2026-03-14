import uuid

import pytest
from httpx import AsyncClient, ASGITransport

from test import LANGUAGES, USER, USER_INFO
from test.api_test import BaseTestEndpoint

@pytest.mark.asyncio
class TestUserEndpoints(BaseTestEndpoint):

    async def login(self):
        async with (
            AsyncClient(
                transport=ASGITransport(app=self.app),
                base_url="http://test"
            ) as client
        ):
            resp = await client.post(
                "/api/user/login",
                json=USER.model_dump(mode="json")
            )

        return resp

    async def register(self, user_id: uuid.UUID | None = None):
        user = USER
        user.id = user_id
        async with (
            AsyncClient(
                transport=ASGITransport(app=self.app),
                base_url="http://test"
            ) as client
        ):
            resp = await client.put(
                "/api/user/register",
                json=user.model_dump(mode="json")
            )

        return resp

    async def test_get_users(self, initialize_user, initialize_user_2):
        async with (
            AsyncClient(
                transport=ASGITransport(app=self.app),
                base_url="http://test"
            ) as client
        ):
            resp = await client.get("/api/user/all_users")

        print(resp.json())


    async def test_login_not_found(self, setup_app):
        resp = await self.login()
        assert resp.status_code == 404
        assert resp.json()["detail"] == "User not found"

    async def test_login_found(self, initialize_user):
        resp = await self.login()
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == USER.user_id
        assert data["telegram_id"] == USER.telegram_id
        assert data["language"] == USER.language

    async def test_register(self, setup_app):
        resp = await self.register()
        assert resp.status_code == 200
        data = resp.json()
        assert data["telegram_id"] == USER.telegram_id
        assert data["language"] == USER.language

    async def test_register_user_exists_failed(self, initialize_user):
        resp = await self.register(USER.id)
        assert resp.status_code == 400
        assert resp.json()["detail"]["message"] == "User already exists"
        received_user = resp.json()["detail"]["user"]
        assert received_user["id"] == USER.user_id
        assert received_user["telegram_id"] == USER.telegram_id
        assert received_user["language"] == USER.language

    async def test_change_user_language(self, initialize_user):
        user = USER
        user.language = LANGUAGES[1]
        async with (
            AsyncClient(
                transport=ASGITransport(app=self.app),
                base_url="http://test"
            ) as client
        ):
            resp = await client.put(
                "/api/user/change_language",
                json=user.model_dump(mode="json")
            )

        assert resp.status_code == 202

    async def test_calculate_calorie(self, initialize_user, update_user_info):
        async with (
            AsyncClient(
                transport=ASGITransport(app=self.app),
                base_url="http://test"
            ) as client
        ):
            resp = await client.post(
                "/api/user/calculate_calorie",
                json=USER_INFO.model_dump(mode="json")
            )

            assert resp.status_code == 200
            assert resp.json()["bmr"] == 2751

    async def test_update_user(self, initialize_user):
        async with (
            AsyncClient(
                transport=ASGITransport(app=self.app),
                base_url="http://test"
            ) as client
        ):
            resp = await client.put(
                "/api/user/update_info",
                json=USER_INFO.model_dump(mode="json")
            )

        assert resp.status_code == 202

