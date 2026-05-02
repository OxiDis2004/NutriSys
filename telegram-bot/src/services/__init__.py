import logging
import os
import uuid
from enum import Enum
from uuid import UUID

from httpx import AsyncClient
from requests import Response

logger = logging.getLogger(__name__)
HOSTNAME = None
PORT = 8000
CLIENT: AsyncClient = None

class ServerEndpoint(Enum):
    USERS = "/user/all_users"
    LOGIN = "/user/login"
    REGISTER = "/user/register"
    CHANGE_LANGUAGE = "/user/change_language"
    UPDATE_INFO = "/user/update_info"
    ADD_WATER = "/water/add"
    STATISTIC_WATER = "/water/{stat_type}"
    ADD_FOOD = "/food/add"
    STATISTIC_FOOD = "/food/{stat_type}"

def get_hostname():
    global HOSTNAME
    HOSTNAME = os.getenv('SERVER_HOST', 'localhost')
    return HOSTNAME

def initialize_client():
    global CLIENT
    CLIENT = AsyncClient(
        base_url=f"http://{HOSTNAME}:{PORT}/api",
        headers={"Authorization": f"Bearer"}
    )


async def request_get(
        url,
        user_id: str | str = None,
        request_id: UUID = uuid.uuid4(),
        throw_error: bool = True
) -> Response:
    logger.debug("Request user=%s | request=%s", user_id, request_id)

    if user_id is not None:
        CLIENT.headers["User-ID"] = str(user_id)
    CLIENT.headers["X-Request-ID"] = str(request_id)
    resp = await CLIENT.get(url=url)
    if throw_error:
        resp.raise_for_status()
    return resp


async def request_post(
        url,
        body,
        user_id: str = None,
        request_id: UUID = uuid.uuid4(),
        throw_error: bool = True
) -> Response:
    logger.debug("Request user=%s | request=%s | body=%s", user_id, request_id, body)

    if user_id is not None:
        CLIENT.headers["User-ID"] = str(user_id)
    CLIENT.headers["X-Request-ID"] = str(request_id)
    resp = await CLIENT.post(url=url, json=body)
    if throw_error:
        resp.raise_for_status()
    return resp


async def request_put(
        url,
        body,
        user_id: str = None,
        request_id: UUID = uuid.uuid4(),
        throw_error: bool = True
) -> Response:
    logger.debug("Request user=%s | request=%s | body=%s", user_id, request_id, body)

    if user_id is not None:
        CLIENT.headers["User-ID"] = str(user_id)
    CLIENT.headers["X-Request-ID"] = str(request_id)
    resp = await CLIENT.put(url=url, json=body)
    if throw_error:
        resp.raise_for_status()
    return resp


async def request_put_image(
        url,
        data,
        files,
        user_id: str,
        request_id: UUID = uuid.uuid4(),
) -> Response:
    logger.debug("Request image user=%s | request=%s | body=%s", user_id, request_id, data)

    CLIENT.headers["User-ID"] = str(user_id)
    CLIENT.headers["X-Request-ID"] = str(request_id)
    return await CLIENT.put(url=url, data=data, files=files)
