import time

from fastapi import HTTPException, Request

REQUEST_LIMIT = {}
MAX_REQUESTS = 1000
WINDOW_SEC = 30


async def rate_limiter(request: Request):
    """Limit the number of requests from a single client IP address.

    Stores request timestamps in memory and rejects requests when the number of
    requests exceeds the configured limit within the time window.

    Args:
        request (Request): Incoming FastAPI request.

    Raises:
        HTTPException: If the client exceeds the allowed request limit.
    """

    ip = request.client.host
    now = time.time()

    if ip not in REQUEST_LIMIT:
        REQUEST_LIMIT[ip] = []

    REQUEST_LIMIT[ip] = [t for t in REQUEST_LIMIT[ip] if now - t < WINDOW_SEC]
    REQUEST_LIMIT[ip].append(now)

    if len(REQUEST_LIMIT[ip]) > MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Too many requests")
