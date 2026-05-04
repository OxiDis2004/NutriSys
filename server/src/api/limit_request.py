from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class LimitRequestSizeMiddleware(BaseHTTPMiddleware):
    """Middleware that rejects requests with a body larger than allowed.

    Attributes:
        max_upload_size (int): Maximum accepted request body size in bytes.
    """

    def __init__(self, app, max_upload_size: int):
        """Initialize request size middleware.

        Args:
            app: ASGI application instance.
            max_upload_size (int): Maximum accepted body size in bytes.
        """

        super().__init__(app)
        self.max_upload_size = max_upload_size

    async def dispatch(self, request: Request, call_next):
        """Validate request body size before passing it to the next handler.

        Args:
            request (Request): Incoming request.
            call_next: Next middleware or route handler.

        Returns:
            Response: Error response if the body is too large, otherwise the next
            handler response.
        """

        body = await request.body()
        if len(body) > self.max_upload_size:
            return Response(
                status_code=413, content={ "detail": "Request body too large" }
            )
        return await call_next(request)
