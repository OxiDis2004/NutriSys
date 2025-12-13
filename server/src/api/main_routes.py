from fastapi import APIRouter, Depends, Response

from src.dependencies import get_db_service

router = APIRouter()

@router.get("/")
async def index():
    return Response(content="Hello world", status_code=200)

@router.get("/db_health")
async def db_health_check(service=Depends(get_db_service)):
    try:
        service.check_health()
        return Response(content="Healthy", status_code=200)
    except Exception as e:
        return Response(content=f"Unhealthy - {str(e)}", status_code=403)
