from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBAdapter:
    def __init__(self, host, port, user, pwd, database):
        from src.models.entity.base import Base
        url = f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{database}"
        self.engine = create_engine(url, echo=True)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        import src.models.entity.language
        import src.models.entity.user
        import src.models.entity.food
        import src.models.entity.drunk_water
        import src.models.entity.sent_food

        Base.metadata.create_all(self.engine)
