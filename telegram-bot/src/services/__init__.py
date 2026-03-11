import os
from requests import Response

HOSTNAME = 'localhost'
PORT = 8000

def get_hostname():
    global HOSTNAME
    # HOSTNAME = os.getenv('SERVER_HOST')

def server():
    return f"http://{HOSTNAME}:{PORT}"

async def request(method, url, body, throw_error: bool = True) -> Response:
    response = await method(url=url, json=body)
    if throw_error:
        response.raise_for_status()
    return response