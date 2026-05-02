import logging
import uuid
from datetime import date

from aiogram.fsm.context import FSMContext

from src.models.dto.water_response import WaterResponseDTO
from src.models.statistic_type import PeriodType
from src.services import request_put, request_post, ServerEndpoint
from src.services.users import get_user_id

logger = logging.getLogger()


async def water_add_request(
        state: FSMContext,
        drunk_water: int
) -> WaterResponseDTO:
    request_id = uuid.uuid4()

    logger.debug(
        "Water add request started | request_id=%s | drunk_water=%s",
        request_id, drunk_water
    )

    try:
        user_id = await get_user_id(state)
        body = { "user_id": user_id, "drunk_water": drunk_water }
        data = (
            await request_put(
                ServerEndpoint.ADD_WATER.value,
                body,
                user_id=user_id
            )
        ).json()

        logger.info(
            "Water added successfully | request_id=%s | user_id=%s | drunk_water=%s",
            request_id, user_id, drunk_water
        )

        return WaterResponseDTO(
            day=data.get("day", date.today()),
            drunk_water=data.get("drunk_water", 0)
        )

    except Exception:
        logger.error("Water add request failed | request_id=%s", request_id)
        raise


async def water_statistic(
        user_id: str | None,
        period_type: PeriodType,
        stat_day: date
) -> list[WaterResponseDTO]:

    request_id = uuid.uuid4()

    logger.debug(
        "Water statistic request started | request_id=%s | user_id=%s | period=%s | date=%s",
        request_id, user_id, period_type.value, stat_day
    )

    if user_id is None:
        logger.warning("Water statistic skipped: user_id is None | request_id=%s", request_id)
        return []

    try:
        body = { "user_id": user_id, "statistic_date": stat_day.isoformat() }
        url = ServerEndpoint.STATISTIC_WATER.value.format(stat_type=period_type.value)

        data = (
            await request_post(
                url,
                body,
                user_id=user_id
            )
        ).json()

        logger.info(
            "Water statistic fetched successfully | request_id=%s | user_id=%s | records=%s",
            request_id, user_id, len(data)
        )

        return [
            WaterResponseDTO(
                day=item.get("day", date.today().isoformat()),
                drunk_water=item.get("drunk_water", 0)
            )
            for item in data
        ]

    except Exception:
        logger.error(
            "Water statistic request failed | request_id=%s | user_id=%s",
            request_id, user_id
        )
        raise


def water_data(
        result: list[WaterResponseDTO],
        date_format
) -> dict:

    try:
        formatted = {
            date.fromisoformat(item.day).strftime(date_format): item.drunk_water
            for item in result
        }

        logger.debug(
            "Water data formatted successfully | records=%s",
            len(formatted)
        )

        return formatted

    except Exception:
        logger.error("Failed to format water data: %s", result)
        raise
