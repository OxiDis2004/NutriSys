from httpx import AsyncClient
from requests import Response

HOSTNAME = 'localhost'
PORT = 8000
CLIENT: AsyncClient = None

def get_hostname():
    global HOSTNAME
    # HOSTNAME = os.getenv('SERVER_HOST')

def server():
    return f"http://{HOSTNAME}:{PORT}"

def initialize_client():
    global CLIENT
    CLIENT = AsyncClient(
        base_url=f"http://{HOSTNAME}:{PORT}/api",
        headers={"Authorization": f"Bearer"}
    )

async def request_get(url, throw_error: bool = True):
    resp = await CLIENT.get(url=url)
    if throw_error:
        resp.raise_for_status()
    return resp

async def request_post(url, body, throw_error: bool = True):
    resp = await CLIENT.post(url=url, json=body)
    if throw_error:
        resp.raise_for_status()
    return resp

async def request_put(url, body, throw_error: bool = True):
    resp = await CLIENT.put(url=url, json=body)
    if throw_error:
        resp.raise_for_status()
    return resp

async def request(method, url, body, throw_error: bool = True) -> Response:
    response = await method(url=url, json=body)
    if throw_error:
        response.raise_for_status()
    return response