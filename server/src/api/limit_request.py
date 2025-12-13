from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response


class LimitRequestSizeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_upload_size: int):
        super().__init__(app)
        self.max_upload_size = max_upload_size

    async def dispatch(self, request: Request, call_next):
        body = await request.body()
        if len(body) > self.max_upload_size:
            return Response(
                status_code=413,
                content={"detail": "Request body too large"}
            )
        return await call_next(request)