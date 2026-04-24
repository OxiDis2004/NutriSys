from fastapi import FastAPI
from fastapi.params import Depends

from src.api import main_router, user_router, water_router, food_router
from src.api.limit_request import LimitRequestSizeMiddleware
from src.api.rate_limiter import rate_limiter
from src.dependencies import initialize_services


def create_app() -> FastAPI:
    app = FastAPI()
    initialize_services()
    app.add_middleware(LimitRequestSizeMiddleware, max_upload_size=65536)
    app_dependency = [Depends(rate_limiter)]

    app.include_router(main_router.router, dependencies=app_dependency)
    app.include_router(user_router.router, dependencies=app_dependency)
    app.include_router(water_router.router, dependencies=app_dependency)
    app.include_router(food_router.router, dependencies=app_dependency)

    return app
