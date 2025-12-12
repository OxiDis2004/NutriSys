from fastapi import APIRouter, Depends

from src.dependencies import get_user_service
from src.models.dto.user_dto import UserDTO
from src.models.dto.user_info_dto import UserInfoDTO

router = APIRouter()

@router.post("/user/login", response_model=UserDTO)
async def login(user: UserDTO, service=Depends(get_user_service)):
    return service.login(user)

@router.put("/user/register", response_model=UserDTO)
async def register(user: UserDTO, service=Depends(get_user_service)):
    return service.register(user)

@router.post("/user/calculate_calorie")
async def calculate_calorie(user: UserInfoDTO, service=Depends(get_user_service)):
    return service.calculate_calorie(user)

@router.put("/user/update_info")
async def update_info(user: UserInfoDTO, service=Depends(get_user_service)):
    return service.update_information(user)
