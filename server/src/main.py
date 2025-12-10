from fastapi import FastAPI

from src.dependencies import set_services, create_db_engine
from src.api import main_routes, user_routes
from src.services.db_service import DBService
from src.services.user_service import UserService

app = FastAPI()

engine = create_db_engine()
db_service = DBService(engine)
user_service = UserService(db_service)

set_services(db_service, user_service)

app.include_router(main_routes.router)

app.include_router(user_routes.router)