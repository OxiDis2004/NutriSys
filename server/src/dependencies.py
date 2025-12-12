from sqlalchemy import create_engine
from src.models.adapter.database_adapter import DBAdapter
from src.services.db_service import DBService
from src.services.user_service import UserService

class ServiceContainer:
    db_service: DBService | None = None
    user_service: UserService | None = None

services = ServiceContainer()

def set_services(db_service: DBService, user_service: UserService):
    services.db_service = db_service
    services.user_service = user_service

def get_db_service() -> DBService:
    return services.db_service

def get_user_service() -> UserService:
    return services.user_service

def initialize_db_service(engine):
    return DBService(engine)

def initialize_user_service(db_service: DBService):
    return UserService(db_service)

def create_db_engine():
    db_host = DBService.get_db_host()
    db_port = DBService.get_db_port()
    db_user = DBService.get_db_user()
    db_pwd = DBService.get_db_pwd()
    database = DBService.get_db_database()

    url = DBAdapter.get_url(db_host, db_port, db_user, db_pwd, database)
    return create_engine(url, echo=True)