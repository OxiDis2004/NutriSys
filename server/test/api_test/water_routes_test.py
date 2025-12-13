import importlib

import pytest
from sqlalchemy import create_engine

from src.dependencies import get_db_service


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