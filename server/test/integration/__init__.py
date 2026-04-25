from datetime import datetime

import pytest
from sqlalchemy import create_engine

from src.services.db_service import DBService
from test import LANGUAGES, USER


class BaseTestService:
    @pytest.fixture(scope="function", autouse=True)
    def setup_database(self):
        engine_mock = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
        )
        self.db_service = DBService(engine_mock)

        yield

        self.db_service = None

    @pytest.fixture
    def initialize_language(self, setup_database):
        self.db_service.add_language(LANGUAGES[0])

    @pytest.fixture
    def initialize_user(self, setup_database):
        self.db_service.add_user(USER, datetime.today())
