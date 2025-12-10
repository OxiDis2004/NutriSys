from fastapi import APIRouter, Depends

from src.dependencies import get_user_service
from src.models.dto.user_dto import UserDTO

router = APIRouter()

@router.post("/user/login", response_model=UserDTO)
async def login(user: UserDTO, service=Depends(get_user_service)):
    return service.login(user)

@router.post("/user/register", response_model=UserDTO)
async def register(user: UserDTO, service=Depends(get_user_service)):
    return service.register(user)
