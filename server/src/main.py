from fastapi import FastAPI
from fastapi.params import Depends

from src.api.limit_request import LimitRequestSizeMiddleware
from src.api.rate_limiter import rate_limiter
from src.dependencies import (
    create_db_engine,
    initialize_db_service,
    initialize_user_service,
    initialize_water_service,
    initialize_ai_service,
    initialize_food_service,
    set_services,
)
from src.api import main_routes, user_routes, water_routes


def create_app() -> FastAPI:
    app = FastAPI()

    engine = create_db_engine()
    db_service = initialize_db_service(engine)
    user_service = initialize_user_service(db_service)
    water_service = initialize_water_service(db_service)
    ai_service = initialize_ai_service()
    food_service = initialize_food_service(db_service, ai_service)

    set_services(db_service, user_service, water_service, ai_service, food_service)

    app.add_middleware(LimitRequestSizeMiddleware, max_upload_size=65536)

    app_dependency = [Depends(rate_limiter)]

    app.include_router(main_routes.router, dependencies=app_dependency)
    app.include_router(user_routes.router, dependencies=app_dependency)
    app.include_router(water_routes.router, dependencies=app_dependency)

    return app