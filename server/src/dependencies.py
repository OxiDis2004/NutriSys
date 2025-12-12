from sqlalchemy import create_engine
from src.models.adapter.database_adapter import DBAdapter
from src.services.ai_service import AIService
from src.services.db_service import DBService
from src.services.food_service import FoodService
from src.services.user_service import UserService
from src.services.water_service import WaterService


class ServiceContainer:
    db_service: DBService | None = None
    user_service: UserService | None = None
    water_service: WaterService | None = None
    ai_service: AIService | None = None
    food_service: FoodService | None = None

services = ServiceContainer()

def set_services(
        db_service: DBService,
        user_service: UserService,
        water_service: WaterService,
        ai_service: AIService,
        food_service: FoodService
):
    services.db_service = db_service
    services.user_service = user_service
    services.water_service = water_service
    services.ai_service = ai_service
    services.food_service = food_service

def get_db_service() -> DBService:
    return services.db_service

def get_user_service() -> UserService:
    return services.user_service

def get_water_service() -> WaterService:
    return services.water_service

def get_ai_service() -> AIService:
    return services.ai_service

def get_food_service() -> FoodService:
    return services.food_service

def initialize_db_service(engine):
    return DBService(engine)

def initialize_user_service(db_service: DBService):
    return UserService(db_service)

def initialize_water_service(db_service: DBService):
    return WaterService(db_service)

def initialize_ai_service():
    return AIService()

def initialize_food_service(db_service: DBService, ai_service: AIService):
    return FoodService(db_service, ai_service)

def create_db_engine():
    db_host = DBService.get_db_host()
    db_port = DBService.get_db_port()
    db_user = DBService.get_db_user()
    db_pwd = DBService.get_db_pwd()
    database = DBService.get_db_database()

    url = DBAdapter.get_url(db_host, db_port, db_user, db_pwd, database)
    return create_engine(url, echo=True)