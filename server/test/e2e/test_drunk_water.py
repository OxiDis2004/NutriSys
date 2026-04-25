import asyncio
import datetime
import random

from pytest_bdd import given, parsers, scenarios, then, when

from src.dependencies import get_services
from src.models.dto.statistic_request_dto import StatisticRequestDTO
from src.models.dto.water_request_dto import WaterRequestDTO
from src.models.dto.water_response_dto import WaterResponseDTO
from src.services.water_service import WaterService

scenarios("features/drunk_water.feature")


@given("remove data in table")
def remove_water_data(states):
    if "user_id" in states:
        get_services().db_service.delete_drunk_water(states["user_id"])
        states["data_exists"] = "false"


@given("add data in table")
def add_water_data(states):
    if "user_id" not in states:
        return

    if states.get("data_exists") == "true":
        return

    current_date = datetime.date(2025, 1, 1)
    end_date = datetime.date(2025, 12, 31)

    water_values = [1500, 2000, 2500, 3000]
    states["water_data"]: list[WaterResponseDTO] = []

    while current_date <= end_date:
        water = random.choice(water_values)
        get_services().db_service.add_drunk_water(
            user_id=states["user_id"], drunk_water=water, _date=current_date
        )
        states["water_data"].append(
            WaterResponseDTO(day=current_date.isoformat(), drunk_water=water)
        )

        current_date += datetime.timedelta(days=1)

    states["data_exists"] = "true"


@given(parsers.cfparse("today user already drank {water_drunk:d} ml"))
def add_water_today(states, water_drunk):
    day = datetime.date.today()
    states["day_water"] = [
        WaterResponseDTO(day=day.isoformat(), drunk_water=water_drunk)
    ]
    get_services().db_service.add_drunk_water(
        user_id=states["user_id"], drunk_water=water_drunk, _date=day
    )


@given(parsers.cfparse("at this week user drunk"))
def add_water_in_week(states):
    current_day = datetime.date(2025, 12, 2)
    states["week"] = current_day
    water_data: list[WaterResponseDTO] = states["water_data"]
    period = WaterService.get_week(current_day)
    states["week_water"] = [
        d for d in water_data if period.start_date <= d.day <= period.end_date
    ]


@given(parsers.cfparse("user drunk almost days in month"))
def add_water_in_month(states):
    current_day = datetime.date(2025, 10, 14)
    states["month"] = current_day
    water_data: list[WaterResponseDTO] = states["water_data"]
    period = WaterService.get_month(current_day)
    states["month_water"] = [
        d for d in water_data if period.start_date <= d.day <= period.end_date
    ]


@given(parsers.cfparse("user drunk in almost days in year"))
def add_water_in_year(states):
    states["year"] = datetime.date(2025, 10, 14)
    assert "water_data" in states and len(states["water_data"]) > 0


@when(parsers.cfparse("I add {water_drunk:d} ml of water"))
def add_water_api(client, states, water_drunk):
    user_id = states.get("user_id", None)

    async def inner():
        response = await client.put(
            "/water/add",
            json=WaterRequestDTO(user_id=user_id, drunk_water=water_drunk).model_dump(
                mode="json"
            ),
        )
        states["response"] = response

    asyncio.run(inner())


@when("get daily statistic")
def get_daily_stats(client, states):
    user_id = states.get("user_id", None)

    async def inner():
        response = await client.post(
            "/water/statistic/day",
            json=StatisticRequestDTO(
                user_id=user_id,
                statistic_date=datetime.date.today(),
            ).model_dump(mode="json"),
        )
        states["response"] = response

    asyncio.run(inner())


@when("get weekly statistic")
def get_weekly_stats(client, states):
    user_id = states.get("user_id", None)

    async def inner():
        response = await client.post(
            "/water/statistic/week",
            json=StatisticRequestDTO(
                user_id=user_id,
                statistic_date=states["week"].strftime("%d_%m_%Y")
            ).model_dump(mode="json"),
        )
        states["response"] = response

    asyncio.run(inner())


@when("get monthly statistic")
def get_monthly_stats(client, states):
    user_id = states.get("user_id", None)

    async def inner():
        response = await client.post(
            "/water/statistic/month",
            json=StatisticRequestDTO(
                user_id=user_id,
                statistic_date=states["month"].strftime("%d_%m_%Y")
            ).model_dump(mode="json"),
        )
        states["response"] = response

    asyncio.run(inner())


@when("get yearly statistic")
def get_yearly_stats(client, states):
    user_id = states.get("user_id", None)

    async def inner():
        response = await client.post(
            "/water/statistic/year",
            json=StatisticRequestDTO(
                user_id=user_id,
                statistic_date=states["year"]
            ).model_dump(mode="json"),
        )
        states["response"] = response

    asyncio.run(inner())


@then(parsers.cfparse("total drunk water should be {water_drunk:d} ml today"))
def check_drunk_water(states, water_drunk):
    assert states["response"].json()["drunk_water_day"] == water_drunk


@then(parsers.cfparse("{type_statistic} statistic"))
def stats(states, type_statistic):
    global min_count, max_count, key
    body = states.get("response").json()

    match type_statistic:
        case "daily":
            min_count = 1
            max_count = 1
            key = "day_water"
        case "weekly":
            min_count = 1
            max_count = 7
            key = "week_water"
        case "monthly":
            min_count = 1
            max_count = 31
            key = "month_water"
        case "yearly":
            min_count = 1
            max_count = 365
            key = "year_water"

    assert min_count <= len(body) <= max_count
    state_water = states.get(key)
    for idx in range(len(body)):
        assert body[idx].get("day") == state_water[idx].day.isoformat()
        assert body[idx].get("drunk_water_day") == state_water[idx].drunk_water
