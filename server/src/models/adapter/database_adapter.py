import logging

from sqlalchemy import Engine, inspect
from sqlalchemy.orm import scoped_session, sessionmaker

logger = logging.getLogger("DatabaseAdapter")

class DBAdapter:
    def __init__(self, engine: Engine):
        self.engine: Engine = engine
        self.session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        )
        logger.info("Database initialized")

    def fetch(self, stmt):
        logger.debug("Executing fetch statement: %s", stmt)

        try:
            with self.session() as curr_session:
                result = curr_session.execute(stmt).fetchall()
                logger.info("Fetch completed. Rows count: %s", len(result))
                return result

        except Exception:
            logger.error("Error while executing fetch statement")
            raise

    def fetch_one(self, stmt):
        logger.debug("Executing fetch_one statement: %s", stmt)

        try:
            with self.session() as curr_session:
                result = curr_session.execute(stmt).first()
                logger.info("Fetch_one completed. Result found: %s", result is not None)
                return result

        except Exception:
            logger.error("Error while executing fetch_one statement")
            raise

    def commit(self, stmt):
        logger.debug("Executing commit statement: %s", stmt)

        with self.session() as curr_session:
            try:
                curr_session.execute(stmt)
                curr_session.commit()
                logger.info("Statement committed successfully")

            except Exception as err:
                curr_session.rollback()
                logger.error("Error committing statement. Transaction rolled back")
                raise Exception("Error committing statement") from err

    def get_pk_constraint_of_table(self, tablename):
        logger.debug("Getting primary key constraint for table: %s", tablename)

        try:
            _inspect = inspect(self.engine)
            pk_name = _inspect.get_pk_constraint(tablename)["name"]

            logger.debug(
                "Primary key constraint for table %s: %s",
                tablename,
                pk_name
            )

            return pk_name

        except Exception:
            logger.error(
                "Error while getting primary key constraint for table: %s",
                tablename
            )
            raise

    def init_db(self):
        logger.debug("Database initialization started")

        try:
            from src.models.entity.base import Base
            from src.models.entity import (
                language,
                user,
                user_info,
                food,
                drunk_water,
                sent_food,
            )
            Base.metadata.create_all(self.engine)
            logger.info("Database tables created successfully")

        except Exception:
            logger.error("Database initialization failed")
            raise

    def close_session(self):
        logger.debug("Closing database session")
        self.session.remove()
        logger.info("Database session closed")

    @staticmethod
    def get_url(host, port, user, pwd, database):
        logger.debug(
            "Creating database URL for host=%s, port=%s, database=%s, user=%s",
            host, port, database, user
        )

        return f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{database}"
