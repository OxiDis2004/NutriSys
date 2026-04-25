import importlib
from datetime import datetime

import pytest
from sqlalchemy import create_engine

from src.dependencies import get_services
from test import USER, USER2, USER_INFO


@pytest.mark.asyncio
class BaseTestEndpoint:
    @pytest.fixture
    def setup_app(self, mocker):
        engine_mock = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
        )
        mocker.patch("src.dependencies.create_db_engine", return_value=engine_mock)
        import src.main

        importlib.reload(src.main)
        from src.main import create_app

        self.app = create_app()

        yield

        self.app = None
        get_services().db_service.close_session()

    @pytest.fixture
    def initialize_user(self, setup_app):
        get_services().db_service.add_user(USER, datetime.today())

    @pytest.fixture
    def initialize_user_2(self, setup_app):
        get_services().db_service.add_user(USER2, datetime.today())

    @pytest.fixture
    def update_user_info(self, setup_app):
        get_services().db_service.update_user_info(USER_INFO)
