import asyncio

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pytest_bdd import given, parsers, then
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


@given(parsers.cfparse('system has no user with telegram id "{telegram_id}"'))
def clear_user(create_test_app, telegram_id):
    get_db_service()._delete_user(telegram_id)


@given(parsers.cfparse('system has user with telegram id "{telegram_id}" and language "{'
                       'language}"'))
def create_user(client, states, telegram_id, language):
    async def inner():
        if len(get_db_service().get_languages()) < 1:
            get_db_service()._add_language(1, "ua")

        response = await client.post("/user/login", json={
            "telegram_id": telegram_id
        })

        if response.status_code == 404:
            response = await client.put("/user/register", json={
                "telegram_id": telegram_id,
                "language": language
            })

        states["user_id"] = response.json()["id"]

    asyncio.run(inner())


@then(parsers.cfparse("response status {status:d}"))
def check_status(states, status):
    ok = states["response"].status_code == status
    if not ok:
        print(states["response"].json()["detail"])
    assert ok == True

@then(parsers.cfparse('with message "{msg}"'))
def check_message(states, msg):
    assert states["response"].json()["detail"] == msg


@pytest.fixture(scope="function")
def after_all():
    yield
    get_db_service().close_session()