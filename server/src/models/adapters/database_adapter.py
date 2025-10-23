from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBAdapter:
    def __init__(self, host, port, user, pwd, database):
        url = f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{database}"
        engine = create_engine(url, echo=True)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=engine)