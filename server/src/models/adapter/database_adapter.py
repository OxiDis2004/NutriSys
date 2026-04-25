from sqlalchemy import Engine, inspect
from sqlalchemy.orm import scoped_session, sessionmaker


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
            except Exception as err:
                curr_session.rollback()
                raise Exception("Error committing statement") from err

    def get_pk_constraint_of_table(self, tablename):
        _inspect = inspect(self.engine)
        return _inspect.get_pk_constraint(tablename)["name"]

    def init_db(self):
        from src.models.entity.base import Base

        Base.metadata.create_all(self.engine)

    def close_session(self):
        self.session.remove()

    @staticmethod
    def get_url(host, port, user, pwd, database):
        return f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{database}"
