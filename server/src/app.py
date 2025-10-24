import os

from fastapi import FastAPI
from sqlalchemy import text

from src.models.adapter.database_adapter import DBAdapter

db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_pwd = os.getenv('DB_PASSWORD')
database = os.getenv('DB_DATABASE')

db = DBAdapter(db_host, db_port, db_user, db_pwd, database)
app = FastAPI()

@app.get("/")
async def index():
    return { "message": f"{db.session}" }

@app.get("/hello")
async def hello():
    return { "message": "hello" }

@app.get("/health")
async def health_check():
    try:
        # Попытка выполнить простой запрос к базе
        with db.session() as session:
            session.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}