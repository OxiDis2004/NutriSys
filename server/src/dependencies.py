from sqlalchemy import create_engine

from src.models.adapter.database_adapter import DBAdapter
from src.services.ai_service import AIService
from src.services.db_service import DBService
from src.services.food_service import FoodService
from src.services.user_service import UserService
from src.services.water_service import WaterService


class ServiceContainer:
    """Container for lazy initialization of application services.

    Stores shared service instances and creates them only when they are first
    requested. This class centralizes dependency management for API routes and
    business services.

    Attributes:
       _db_service (DBService | None): Database access service.
       _user_service (UserService | None): User business logic service.
       _water_service (WaterService | None): Water tracking service.
       _ai_service (AIService | None): AI recognition service.
       _food_service (FoodService | None): Food business logic service.
    """
    _db_service: DBService = None
    _user_service: UserService = None
    _water_service: WaterService = None
    _ai_service: AIService = None
    _food_service: FoodService = None

    def __init__(self, engine):
        """Initialize the service container.

        Args:
            engine: SQLAlchemy engine used by database-related services.
        """
        self._engine = engine

    @property
    def db_service(self) -> DBService:
        """Return the database service instance.

        Lazily creates the database service and initializes supported languages
        before returning it.

        Returns:
            DBService: Database service instance.
        """
        if self._db_service is None:
            self._db_service = DBService(self._engine)
            self._db_service.initialize_languages()
        return self._db_service

    @property
    def user_service(self) -> UserService:
        """Return the user service instance.

        Returns:
            UserService: Service responsible for user-related business logic.
        """
        if self._user_service is None:
            self._user_service = UserService(self.db_service)
        return self._user_service

    @property
    def ai_service(self) -> AIService:
        """Return the AI service instance.

        Returns:
            AIService: Service responsible for image recognition operations.
        """
        if self._ai_service is None:
            self._ai_service = AIService(self.db_service)
        return self._ai_service

    @property
    def water_service(self) -> WaterService:
        """Return the water service instance.

        Returns:
            WaterService: Service responsible for water tracking operations.
        """
        if self._water_service is None:
            self._water_service = WaterService(self.db_service)
        return self._water_service

    @property
    def food_service(self) -> FoodService:
        """Return the food service instance.

        Returns:
            FoodService: Service responsible for food recognition and nutrition logic.
        """
        if self._food_service is None:
            self._food_service = FoodService(self.db_service, self.ai_service)
        return self._food_service


service_container: ServiceContainer | None = None


def initialize_services():
    """Initialize global application services.

    Creates the database engine and stores a configured ServiceContainer in the
    global service_container variable.
    """
    global service_container
    engine = create_db_engine()
    service_container = ServiceContainer(engine)


def get_services():
    """Return the global service container.

    This function is used as a FastAPI dependency in API routes.

    Returns:
        ServiceContainer | None: Current global service container.
    """
    return service_container


def create_db_engine():
    """Create a SQLAlchemy database engine.

    Reads database connection settings from environment variables through
    DBService helper methods, builds a connection URL and creates the engine.

    Returns:
        Engine: SQLAlchemy database engine.
    """
    db_host = DBService.get_db_host()
    db_port = DBService.get_db_port()
    db_user = DBService.get_db_user()
    db_pwd = DBService.get_db_pwd()
    database = DBService.get_db_database()

    url = DBAdapter.get_url(db_host, db_port, db_user, db_pwd, database)
    return create_engine(url, echo=True)
