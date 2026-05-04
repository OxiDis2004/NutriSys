from fastapi import APIRouter, Depends, Response

from src.dependencies import ServiceContainer, get_services

router = APIRouter(prefix="/api")


@router.get("/")
async def index():
    """Return a basic API health response.

    Returns:
    Response: Plain text response confirming that the API is running.
    """
    return Response(content="Hello world")


@router.get("/db_health")
async def db_health_check(
        services: ServiceContainer = Depends(get_services),  # noqa: B008
):
    """Check database availability.

    Executes a lightweight database health check through DBService.

    Args:
        services (ServiceContainer): Application service container.

    Returns:
        Response: "Healthy" response if the database is available,
        otherwise an "Unhealthy" response.
    """

    try:
        services.db_service.check_health()
        return Response(content="Healthy")
    except Exception as e:
        return Response(content=f"Unhealthy - {str(e)}", status_code=403)
