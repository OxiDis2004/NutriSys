from fastapi import APIRouter, Depends

from src.dependencies import ServiceContainer, get_services
from src.models.dto.user_dto import UserDTO
from src.models.dto.user_info_dto import UserInfoDTO

router = APIRouter(prefix="/api/user")


@router.post("/login", response_model=UserDTO)
async def login(
        user: UserDTO,
        services: ServiceContainer = Depends(get_services),  # noqa: B008
):
    return services.user_service.login(user)


@router.put("/register", response_model=UserDTO)
async def register(
        user: UserDTO,
        services: ServiceContainer = Depends(get_services),  # noqa: B008
):
    return services.user_service.register(user)


@router.put("/change_language", response_model=UserDTO)
async def change_language(
        user: UserDTO,
        services: ServiceContainer = Depends(get_services),  # noqa: B008
):
    return services.user_service.update_language(user)


@router.post("/get_info", response_model=UserInfoDTO)
async def get_info(
        user: UserDTO,
        services: ServiceContainer = Depends(get_services),  # noqa: B008
):
    return services.user_service.get_information(user)


@router.put("/update_info")
async def update_info(
        user: UserInfoDTO,
        services: ServiceContainer = Depends(get_services),  # noqa: B008
):
    return services.user_service.update_information(user)


@router.post("/calculate_bmr")
async def calculate_bmr(
        user: UserDTO,
        services: ServiceContainer = Depends(get_services),  # noqa: B008
):
    return services.user_service.calculate_bmr(user)
