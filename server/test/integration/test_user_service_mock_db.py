import uuid
from datetime import datetime

import pytest
from sqlalchemy import create_engine
from src.services.db_service import DBService
from src.services.user_service import UserService
from src.models.dto.user_dto import UserDTO
from fastapi import HTTPException

class TestUserServiceMockDB:

    @pytest.fixture(scope="function", autouse=True)
    def setup_services(self, mocker):
        self.engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False}
        )
        self.db_service = DBService(self.engine)
        self.user_service = UserService(self.db_service)
        self.get_user_spy = mocker.spy(self.db_service, "get_user")

        yield

        self.engine.dispose()
        self.db_service = None
        self.user_service = None

    def test_login_success(self, setup_services):
        self.db_service._add_language(1, "ua")
        user = UserDTO(id=str(uuid.uuid4()), telegram_id="user123", language="ua")
        self.db_service.add_user(user, datetime.now())

        received_user = self.user_service.login(UserDTO(telegram_id="user123"))

        assert received_user.id == user.id
        assert received_user.language == "ua"

        self.get_user_spy.assert_called_once_with("user123")

    def test_login_not_found(self, setup_services):
        with pytest.raises(HTTPException) as exc_info:
            self.user_service.login(UserDTO(telegram_id="nonexistent"))

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "User not found"

        self.get_user_spy.assert_called_once_with("nonexistent")