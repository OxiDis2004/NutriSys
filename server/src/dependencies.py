from sqlalchemy import create_engine

from src.models.adapter.database_adapter import DBAdapter
from src.services.db_service import DBService

_db_service = None
_user_service = None

def set_services(db_service, user_service):
    global _db_service, _user_service
    _db_service = db_service
    _user_service = user_service

def create_db_engine():
    db_host = DBService.get_db_host()
    db_port = DBService.get_db_port()
    db_user = DBService.get_db_user()
    db_pwd = DBService.get_db_pwd()
    database = DBService.get_db_database()

    url = DBAdapter.get_url(db_host, db_port, db_user, db_pwd, database)
    return create_engine(url, echo=True)

def get_db_service():
    return _db_service

def get_user_service():
    return _user_service
