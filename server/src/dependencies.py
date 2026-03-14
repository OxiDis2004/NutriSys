from sqlalchemy import create_engine
from src.models.adapter.database_adapter import DBAdapter
from src.services.ai_service import AIService
from src.services.db_service import DBService
from src.services.food_service import FoodService
from src.services.user_service import UserService
from src.services.water_service import WaterService


class ServiceContainer:
    _db_service: DBService | None = None
    _user_service: UserService | None = None
    _water_service: WaterService | None = None
    _ai_service: AIService | None = None
    _food_service: FoodService | None = None

    def __init__(self, engine):
        self._engine = engine

    @property
    def db_service(self) -> DBService:
        if self._db_service is None:
            self._db_service = DBService(self._engine)
            self._db_service.initialize_languages()
        return self._db_service

    @property
    def user_service(self) -> UserService:
        if self._user_service is None:
            self._user_service = UserService(self.db_service)
        return self._user_service

    @property
    def ai_service(self) -> AIService:
        if self._ai_service is None:
            self._ai_service = AIService(self.db_service)
        return self._ai_service

    @property
    def water_service(self) -> WaterService:
        if self._water_service is None:
            self._water_service = WaterService(self.db_service)
        return self._water_service

    @property
    def food_service(self) -> FoodService:
        if self._food_service is None:
            self._food_service = FoodService(self.db_service, self.ai_service)
        return self._food_service

service_container: ServiceContainer | None = None

def initialize_services():
    global service_container
    engine = create_db_engine()
    service_container = ServiceContainer(engine)

def get_services():
    return service_container

def create_db_engine():
    db_host = DBService.get_db_host()
    db_port = DBService.get_db_port()
    db_user = DBService.get_db_user()
    db_pwd = DBService.get_db_pwd()
    database = DBService.get_db_database()

    url = DBAdapter.get_url(db_host, db_port, db_user, db_pwd, database)
    return create_engine(url, echo=True)
