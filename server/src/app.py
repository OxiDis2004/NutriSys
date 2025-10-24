import os

from fastapi import FastAPI

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
