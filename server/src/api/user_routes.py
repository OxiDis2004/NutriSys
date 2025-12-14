from fastapi import APIRouter, Depends

from src.dependencies import get_user_service
from src.models.dto.user_dto import UserDTO
from src.models.dto.user_info_dto import UserInfoDTO

router = APIRouter(prefix="/api/user")

@router.post("/login", response_model=UserDTO)
async def login(user: UserDTO, service=Depends(get_user_service)):
    return service.login(user)

@router.put("/change_language", response_model=UserDTO)
async def change_language(user: UserDTO, service=Depends(get_user_service)):
    return service.update_language(user)

@router.put("/register", response_model=UserDTO)
async def register(user: UserDTO, service=Depends(get_user_service)):
    return service.register(user)

@router.post("/calculate_calorie")
async def calculate_calorie(user: UserInfoDTO, service=Depends(get_user_service)):
    return service.calculate_calorie(user)

@router.put("/update_info")
async def update_info(user: UserInfoDTO, service=Depends(get_user_service)):
    return service.update_information(user)
