import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine

from src.dependencies import get_db_service

states_dict = {}

@pytest.fixture(scope="function")
def create_test_app(mocker):
    engine = create_engine("sqlite:///:memory:")
    mocker.patch("src.dependencies.create_db_engine", return_value=engine)
    from src.main import create_app
    app: FastAPI = create_app()
    yield app


@pytest.fixture(scope="function")
def client(create_test_app):
    return AsyncClient(
        transport=ASGITransport(app=create_test_app),
        base_url="http://test"
    )

@pytest.fixture
def states():
    return states_dict


@pytest.fixture(scope="function")
def after_all():
    yield
    get_db_service().close_session()