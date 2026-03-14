from fastapi import APIRouter, Depends

from src.dependencies import get_services, ServiceContainer
from src.models.dto.user_dto import UserDTO
from src.models.dto.user_info_dto import UserInfoDTO

router = APIRouter(prefix="/api/user")

@router.get("/all_users", response_model=list[UserDTO])
async def get_users(services: ServiceContainer = Depends(get_services)):
    return services.user_service.get_users()

@router.post("/login", response_model=UserDTO)
async def login(user: UserDTO, services: ServiceContainer = Depends(get_services)):
    return services.user_service.login(user)

@router.put("/change_language", response_model=UserDTO)
async def change_language(user: UserDTO, services: ServiceContainer = Depends(get_services)):
    return services.user_service.update_language(user)

@router.put("/register", response_model=UserDTO)
async def register(user: UserDTO, services: ServiceContainer = Depends(get_services)):
    return services.user_service.register(user)

@router.post("/calculate_calorie")
async def calculate_calorie(user_info: UserInfoDTO, services: ServiceContainer = Depends(get_services)):
    return services.user_service.calculate_calorie(user_info)

@router.put("/update_info")
async def update_info(user: UserInfoDTO, services: ServiceContainer = Depends(get_services)):
    return services.user_service.update_information(user)
