import uuid
from datetime import datetime
import importlib

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine

from src.dependencies import get_db_service
from test import LANGUAGES, USER, USER_INFO


@pytest.mark.asyncio
class TestUserEndpoints:

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
        for lang in LANGUAGES:
            get_db_service()._add_language(lang)

    @pytest.fixture
    def initialize_user(self, setup_mocks):
        get_db_service().add_user(USER, datetime.today())

    @pytest.fixture
    def update_user_info(self, setup_mocks):
        get_db_service().update_user_info(USER_INFO)

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

    async def test_login_not_found(self, setup_mocks):
        resp = await self.login()
        assert resp.status_code == 404
        assert resp.json()["detail"] == "User not found"

    async def test_login_found(self, initialize_language, initialize_user):
        resp = await self.login()
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == USER.user_id
        assert data["telegram_id"] == USER.telegram_id
        assert data["language"] == USER.language

    async def test_register(self, initialize_language):
        resp = await self.register()
        assert resp.status_code == 200
        data = resp.json()
        assert data["telegram_id"] == USER.telegram_id
        assert data["language"] == USER.language

    async def test_register_user_exists_failed(self, initialize_language, initialize_user):
        resp = await self.register(USER.id)
        assert resp.status_code == 400
        assert resp.json()["detail"]["message"] == "User already exists"
        received_user = resp.json()["detail"]["user"]
        assert received_user["id"] == USER.user_id
        assert received_user["telegram_id"] == USER.telegram_id
        assert received_user["language"] == USER.language

    async def test_change_user_language(self, initialize_language, initialize_user):
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

    async def test_calculate_calorie(self, initialize_language, initialize_user, update_user_info):
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

    async def test_update_user(self, initialize_language, initialize_user):
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

