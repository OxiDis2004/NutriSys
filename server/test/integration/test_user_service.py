import uuid
from datetime import date, datetime

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine

from src.models.dto.user_dto import UserDTO
from src.models.dto.user_info_dto import UserInfoDTO
from src.models.property.activity import Activity
from src.models.property.goal import Goal
from src.services.db_service import DBService
from src.services.user_service import UserService

language_ua = (1, "ua")

user: UserDTO = UserDTO(id=str(uuid.uuid4()), telegram_id="example123", language=language_ua[1])

user_info: UserInfoDTO = UserInfoDTO(id=user.id, name="Denys", lastname="Ponomarenko",
    birthday=date(2005, 1, 6), weight=100, height=182, sex='m',
    count_of_sport_in_week=Activity.HighActivity, goal=Goal.LoseWeight
)

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
        self.db_service._add_language(language_ua[0], language_ua[1])

    @pytest.fixture
    def initialize_user(self, setup_services):
        self.db_service.add_user(user, datetime.today())

    def test_login(self, initialize_language, initialize_user):
        received_user = self.user_service.login(UserDTO(telegram_id=user.telegram_id))
        assert received_user.id == user.id
        assert received_user.telegram_id == user.telegram_id
        assert received_user.language == user.language

    def test_register(self, initialize_language):
        registered_user = self.user_service.register(
            UserDTO(
                telegram_id=user.telegram_id,
                language=user.language
            )
        )
        assert user.id is not None
        assert registered_user.telegram_id == user.telegram_id
        assert registered_user.language == user.language

    def test_update_user(self, initialize_language, initialize_user):
        response = self.user_service.update_information(user_info)
        assert response.status_code == 202

    def test_login_failed(self):
        with pytest.raises(Exception) as e_info:
            self.user_service.login(UserDTO(telegram_id=user.telegram_id))

        assert e_info.errisinstance(HTTPException)
        assert e_info.value.status_code == 404
        assert e_info.value.detail == "User not found"

    def test_register_failed(self, initialize_language, initialize_user):
        with pytest.raises(Exception) as e_info:
            registered_user = self.user_service.register(
                UserDTO(
                    telegram_id=user.telegram_id,
                    language=user.language
                )
            )

        assert e_info.errisinstance(HTTPException)
        assert e_info.value.status_code == 400
        assert e_info.value.detail == "User exists"

    def test_update_information_failed(self, initialize_language):
        with pytest.raises(Exception) as e_info:
            self.user_service.update_information(None)

        assert e_info.errisinstance(HTTPException)
        assert e_info.value.status_code == 400
        assert e_info.value.detail == "User id is undefined"
