import logging
import uuid

import time
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

logger = logging.getLogger("Server")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        user_id = request.headers.get("User-ID", None)
        start_time = time.time()

        logger.info(
            "Incoming request | user_id=%s | request_id=%s | method=%s | url=%s",
            user_id, request_id, request.method, request.url
        )

        try:
            response = await call_next(request)
            process_time = time.time() - start_time

            logger.debug(
                "Request completed | user_id=%s | request_id=%s | method=%s | status=%s | "
                "time=%.3fs",
                user_id, request_id, request.method, response.status_code, process_time
            )

            response.headers["X-Request-ID"] = request_id
            return response

        except Exception as e:
            logger.error(
                "Unhandled server error for request %s: %s",
                request_id, e
            )

            return JSONResponse(
                status_code=500,
                content={
                    "message": f"Internal server error - {e}",
                    "request": request_id
                }
            )
