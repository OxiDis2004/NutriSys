import uvicorn
from fastapi import FastAPI
from fastapi.params import Depends

from src.api import food_router, main_router, user_router, water_router
from src.api.limit_request import LimitRequestSizeMiddleware
from src.api.rate_limiter import rate_limiter
from src.api.request_logging import RequestLoggingMiddleware
from src.dependencies import initialize_services
from src.logger import setup_logger


def create_app() -> FastAPI:
    setup_logger()

    app = FastAPI()
    initialize_services()
    app.add_middleware(LimitRequestSizeMiddleware, max_upload_size=65536)
    app.add_middleware(RequestLoggingMiddleware)
    app_dependency = [Depends(rate_limiter)]

    app.include_router(main_router.router, dependencies=app_dependency)
    app.include_router(user_router.router, dependencies=app_dependency)
    app.include_router(water_router.router, dependencies=app_dependency)
    app.include_router(food_router.router, dependencies=app_dependency)

    return app


if __name__ == "__main__":
    uvicorn.run(
        "src.main:create_app",
        factory=True,
        reload=True
    )
