import uuid
from datetime import datetime, date
import importlib

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine

from src.dependencies import get_db_service
from src.models.dto.user_dto import UserDTO
from src.models.dto.user_info_dto import UserInfoDTO
from src.models.property.activity import Activity
from src.models.property.goal import Goal

language_ua = (1, "ua")
user: UserDTO = UserDTO(id=str(uuid.uuid4()), telegram_id="example123", language=language_ua[1])
user_info: UserInfoDTO = UserInfoDTO(id=user.id, name="Denys", lastname="Ponomarenko",
    birthday=date(2005, 1, 6), weight=100, height=182, sex='m',
    count_of_sport_in_week=Activity.HighActivity, goal=Goal.LoseWeight
)

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

    async def test_login_not_found(self, setup_mocks):
        async with (
            AsyncClient(
                transport=ASGITransport(app=self.app),
                base_url="http://test"
            ) as client
        ):
            resp = await client.post(
                "/user/login",
                json={ "telegram_id": user.telegram_id }
            )

        assert resp.status_code == 404
        assert resp.json() == { "detail": "User not found" }

    @pytest.fixture
    def initialize_language(self, setup_mocks):
        get_db_service()._add_language(language_ua[0], language_ua[1])

    @pytest.fixture
    def initialize_user(self, setup_mocks):
        get_db_service().add_user(user, datetime.today())

    async def test_login_found(self, initialize_language, initialize_user):
        async with (
            AsyncClient(
                transport=ASGITransport(app=self.app),
                base_url="http://test"
            ) as client
        ):
            resp = await client.post(
                "/user/login",
                json={ "telegram_id": user.telegram_id }
            )

        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == user.id
        assert data["telegram_id"] == user.telegram_id
        assert data["language"] == user.language

    async def test_register(self, initialize_language):
        async with (
            AsyncClient(
                transport=ASGITransport(app=self.app),
                base_url="http://test"
            ) as client
        ):
            resp = await client.put(
                "/user/register",
                json={ "telegram_id": user.telegram_id, "language": user.language }
            )

        assert resp.status_code == 200
        data = resp.json()
        assert data["telegram_id"] == user.telegram_id
        assert data["language"] == user.language

    async def test_register_user_exists_failed(self, initialize_language, initialize_user):
        async with (
            AsyncClient(
                transport=ASGITransport(app=self.app),
                base_url="http://test"
            ) as client
        ):
            resp = await client.put(
                "/user/register",
                json={ "telegram_id": user.telegram_id, "language": user.language }
            )

        assert resp.status_code == 400
        assert resp.json() == { "detail": "User exists" }

    async def test_update_user(self, initialize_language, initialize_user):
        print(user_info.model_dump())
        async with (
            AsyncClient(
                transport=ASGITransport(app=self.app),
                base_url="http://test"
            ) as client
        ):
            resp = await client.put(
                "/user/update_info",
                json=user_info.model_dump(mode="json")
            )

        print(resp.status_code)
        assert resp.status_code == 202


