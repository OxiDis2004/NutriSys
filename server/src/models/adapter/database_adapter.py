from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker


class DBAdapter:
    def __init__(self, engine: Engine):
        self.engine: Engine = engine
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def fetch(self, stmt):
        with self.session() as curr_session:
            return curr_session.execute(stmt).fetchall()

    def fetch_one(self, stmt):
        with self.session() as curr_session:
            return curr_session.execute(stmt).first()

    def commit(self, stmt):
        with self.session() as curr_session:
            curr_session.execute(stmt)
            curr_session.commit()

    def init_db(self):
        from src.models.entity.base import Base
        import src.models.entity.language
        import src.models.entity.user
        import src.models.entity.user_info
        import src.models.entity.food
        import src.models.entity.drunk_water
        import src.models.entity.sent_food
        Base.metadata.create_all(self.engine)

    @staticmethod
    def get_url(host, port, user, pwd, database):
        return f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{database}"
