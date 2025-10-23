from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class DBAdapter:
    def __init__(self, host, port, user, pwd, database):
        url = f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{database}"
        self.engine = create_engine(url, echo=True)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        DeclarativeBase.metadata.create_all(self.engine)