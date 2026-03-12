from datetime import datetime

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine

from src.models.dto.user_dto import UserDTO
from src.models.dto.user_info_dto import UserInfoDTO
from src.services.db_service import DBService
from src.services.user_service import UserService
from test import LANGUAGES, USER, USER_INFO


class TestUserService:

    @pytest.fixture(scope="function", autouse=True)
    def setup_services(self):
        self.engine_mock = create_engine(
            f"sqlite:///:memory:",
            connect_args={"check_same_thread": False},
        )
        self.db_service = DBService(self.engine_mock)
        self.user_service = UserService(self.db_service)

        yield

        self.engine_mock = None
        self.db_service = None
        self.user_service = None

    @pytest.fixture
    def initialize_language(self, setup_services):
        self.db_service._add_language(LANGUAGES[0])

    @pytest.fixture
    def initialize_user(self, setup_services):
        self.db_service.add_user(USER, datetime.today())

    def test_login(self, initialize_language, initialize_user):
        received_user = self.user_service.login(
            UserDTO(
                id=None,
                telegram_id=USER.telegram_id,
                language=USER.language
            )
        )
        assert received_user.id == USER.user_id
        assert received_user.telegram_id == USER.telegram_id
        assert received_user.language == USER.language

    def test_register(self, initialize_language):
        registered_user = self.user_service.register(
            UserDTO(
                id=None,
                telegram_id=USER.telegram_id,
                language=USER.language
            )
        )
        assert USER.id is not None
        assert registered_user.telegram_id == USER.telegram_id
        assert registered_user.language == USER.language

    def test_update_user(self, initialize_language, initialize_user):
        response = self.user_service.update_information(USER_INFO)
        assert response.status_code == 202

    def test_login_failed(self):
        with pytest.raises(Exception) as e_info:
            self.user_service.login(UserDTO(id=None, telegram_id=(USER.telegram_id - 1), language=USER.language))

        assert e_info.errisinstance(HTTPException)
        assert e_info.value.status_code == 404
        assert e_info.value.detail == "User not found"

    def test_register_failed(self, initialize_language, initialize_user):
        with pytest.raises(Exception) as e_info:
            self.user_service.register(
                UserDTO(
                    id=None,
                    telegram_id=USER.telegram_id,
                    language=USER.language
                )
            )

        assert e_info.errisinstance(HTTPException)
        assert e_info.value.status_code == 400
        assert e_info.value.detail["message"] == "User already exists"
        assert e_info.value.detail["user"] == USER.model_dump(mode="json")

    def test_update_information_failed(self, initialize_language):
        with pytest.raises(Exception) as e_info:
            self.user_service.update_information(UserInfoDTO(id=None))

        assert e_info.errisinstance(HTTPException)
        assert e_info.value.status_code == 400
        assert e_info.value.detail == "User id is undefined"
