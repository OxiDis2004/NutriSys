from fastapi import FastAPI
from src.dependencies import (
    create_db_engine,
    initialize_db_service,
    initialize_user_service,
    set_services,
)
from src.api import main_routes, user_routes

def create_app() -> FastAPI:
    app = FastAPI()

    engine = create_db_engine()
    db_service = initialize_db_service(engine)
    user_service = initialize_user_service(db_service)

    set_services(db_service, user_service)

    app.include_router(main_routes.router)
    app.include_router(user_routes.router)

    return app