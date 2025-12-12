from sqlalchemy import Engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session


class DBAdapter:
    def __init__(self, engine: Engine):
        self.engine: Engine = engine
        self.session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        )

    def fetch(self, stmt):
        with self.session() as curr_session:
            return curr_session.execute(stmt).fetchall()

    def fetch_one(self, stmt):
        with self.session() as curr_session:
            return curr_session.execute(stmt).first()

    def commit(self, stmt):
        with self.session() as curr_session:
            try:
                curr_session.execute(stmt)
                curr_session.commit()
            except:
                curr_session.rollback()
                raise

    def get_pk_constraint_of_table(self, tablename):
        insp = inspect(self.engine)
        return insp.get_pk_constraint(tablename)["name"]

    def init_db(self):
        from src.models.entity.base import Base
        import src.models.entity.language
        import src.models.entity.user
        import src.models.entity.user_info
        import src.models.entity.food
        import src.models.entity.drunk_water
        import src.models.entity.sent_food
        Base.metadata.create_all(self.engine)

    def close_session(self):
        self.session.remove()

    @staticmethod
    def get_url(host, port, user, pwd, database):
        return f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{database}"
