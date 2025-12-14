import time
from fastapi import HTTPException, Request

REQUEST_LIMIT = {}
MAX_REQUESTS = 1000
WINDOW_SEC = 30

async def rate_limiter(request: Request):
    ip = request.client.host
    api_path = request.url.path
    print(api_path)
    now = time.time()

    if ip not in REQUEST_LIMIT:
        REQUEST_LIMIT[ip] = []

    REQUEST_LIMIT[ip] = [t for t in REQUEST_LIMIT[ip] if now - t < WINDOW_SEC]
    REQUEST_LIMIT[ip].append(now)

    if len(REQUEST_LIMIT[ip]) > MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Too many requests")
