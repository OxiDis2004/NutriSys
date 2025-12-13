import asyncio
from datetime import date

from pytest_bdd import when, parsers, then, scenarios, given

from src.dependencies import get_db_service
from src.models.dto.user_dto import UserDTO
from src.models.dto.user_info_dto import UserInfoDTO
from src.models.property.activity import Activity
from src.models.property.goal import Goal

scenarios("features/user_profile_personalization.feature")

@given(parsers.cfparse('system has language "{language}"'))
def step_impl(language):
    rows = get_db_service().get_languages()
    for row in rows:
        if row.iso == language:
            return

    get_db_service()._add_language(2, language)

@when(parsers.cfparse(
    'user with telegram id "{telegram_id}" updates profile language to "{language}"'
))
def update_language(client, states, telegram_id, language):
    user_id = states["user_id"] if "user_id" in states else None
    states["user_data"] = UserDTO(id=user_id, telegram_id=telegram_id, language=language)

    async def inner():
        response = await client.put(
            "/user/change_language",
            json=states["user_data"].model_dump(mode="json")
        )
        states["response"] = response

    asyncio.run(inner())

@then(parsers.cfparse('user profile language should be "{language}"'))
def check_update(states):
    body = states.get("response").json()
    user_data: UserDTO = states["user_data"]

    assert body.get("id") == user_data.id
    assert body.get("telegram_id") == user_data.telegram_id
    assert body.get("language") == user_data.language


@when("user update profile information")
def update_information(client, states):
    user_id = states["user_id"] if "user_id" in states else None
    user_info: UserInfoDTO = UserInfoDTO(id=user_id, name="Denys", lastname="Ponomarenko",
        birthday=date(2005, 1, 6), weight=100, height=182, sex='m',
        count_of_sport_in_week=Activity.HighActivity, goal=Goal.LoseWeight
    )

    async def inner():
        response = await client.put(
            "/user/update_info",
            json=user_info.model_dump(mode="json")
        )
        states["response"] = response

    asyncio.run(inner())