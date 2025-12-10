from fastapi import APIRouter, Depends
from sqlalchemy import text

from src.dependencies import get_db_service

router = APIRouter()

@router.get("/")
async def index():
    return { "status": "ok", "message": "hello" }

@router.get("/db_health")
async def db_health_check(db=Depends(get_db_service)):
    try:
        with db.session() as session:
            session.execute(text("SELECT 1"))
        return { "status": "ok", "message": "Healthy" }
    except Exception as e:
        return { "status": "error", "message": f"Unhealthy - {str(e)}" }
