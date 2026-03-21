from enum import Enum

from httpx import AsyncClient
from requests import Response

HOSTNAME = 'localhost'
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
    # HOSTNAME = os.getenv('SERVER_HOST')

def initialize_client():
    global CLIENT
    CLIENT = AsyncClient(
        base_url=f"http://{HOSTNAME}:{PORT}/api",
        headers={"Authorization": f"Bearer"}
    )

async def request_get(url, throw_error: bool = True) -> Response:
    resp = await CLIENT.get(url=url)
    if throw_error:
        resp.raise_for_status()
    return resp

async def request_post(url, body, throw_error: bool = True) -> Response:
    resp = await CLIENT.post(url=url, json=body)
    if throw_error:
        resp.raise_for_status()
    return resp

async def request_put(url, body, throw_error: bool = True) -> Response:
    resp = await CLIENT.put(url=url, json=body)
    if throw_error:
        resp.raise_for_status()
    return resp

async def request_put_image(url, data, files) -> Response:
    return await CLIENT.put(url=url, data=data, files=files)
