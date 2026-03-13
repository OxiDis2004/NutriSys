from fastapi import APIRouter, Depends

from src.dependencies import get_services, ServiceContainer
from src.models.dto.water_request_dto import WaterRequestDTO
from src.models.dto.water_response_dto import WaterResponseDTO
from src.models.dto.statistic_request_dto import StatisticRequestDTO

router = APIRouter(prefix="/api/food")

@router.put("/add", response_model=WaterResponseDTO)
async def add_water(water_dto: WaterRequestDTO, services: ServiceContainer = Depends(get_services)):
    return services.food_service

@router.post("/statistic/day", response_model=list[WaterResponseDTO])
async def statistic_week(water_statistic_dto: StatisticRequestDTO, services: ServiceContainer = Depends(get_services)):
    return services.food_service

@router.post("/statistic/week", response_model=list[WaterResponseDTO])
async def statistic_week(water_statistic_dto: StatisticRequestDTO, services: ServiceContainer = Depends(get_services)):
    return services.food_service

@router.post("/statistic/month", response_model=list[WaterResponseDTO])
async def statistic_week(water_statistic_dto: StatisticRequestDTO, services: ServiceContainer = Depends(get_services)):
    return services.food_service

@router.post("/statistic/year", response_model=list[WaterResponseDTO])
async def statistic_week(water_statistic_dto: StatisticRequestDTO, services: ServiceContainer = Depends(get_services)):
    return services.food_service


