from fastapi import APIRouter, Depends, Response

from src.dependencies import get_services, ServiceContainer

router = APIRouter(prefix="/api")

@router.get("/")
async def index():
    return Response(content="Hello world", status_code=200)

@router.get("/db_health")
async def db_health_check(services: ServiceContainer = Depends(get_services)):
    try:
        services.db_service.check_health()
        return Response(content="Healthy", status_code=200)
    except Exception as e:
        return Response(content=f"Unhealthy - {str(e)}", status_code=403)
