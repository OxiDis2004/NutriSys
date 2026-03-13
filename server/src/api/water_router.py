from fastapi import APIRouter, Depends

from src.dependencies import get_services, ServiceContainer
from src.models.dto.water_request_dto import WaterRequestDTO
from src.models.dto.water_response_dto import WaterResponseDTO
from src.models.dto.water_statistic_request_dto import WaterStatisticRequestDTO
from src.models.property.period import PeriodType

router = APIRouter(prefix="/api/water")

@router.put("/add", response_model=WaterResponseDTO)
async def add_water(water_dto: WaterRequestDTO, services: ServiceContainer = Depends(get_services)):
    return services.water_service.add_drunk_water(water_dto)

@router.post("/statistic/day", response_model=list[WaterResponseDTO])
async def statistic_week(water_statistic_dto: WaterStatisticRequestDTO, services: ServiceContainer = Depends(get_services)):
    return services.water_service.statistic(water_statistic_dto, PeriodType.DAY)

@router.post("/statistic/week", response_model=list[WaterResponseDTO])
async def statistic_week(water_statistic_dto: WaterStatisticRequestDTO, services: ServiceContainer = Depends(get_services)):
    return services.water_service.statistic(water_statistic_dto, PeriodType.WEEK)

@router.post("/statistic/month", response_model=list[WaterResponseDTO])
async def statistic_week(water_statistic_dto: WaterStatisticRequestDTO, services: ServiceContainer = Depends(get_services)):
    return services.water_service.statistic(water_statistic_dto, PeriodType.MONTH)

@router.post("/statistic/year", response_model=list[WaterResponseDTO])
async def statistic_week(water_statistic_dto: WaterStatisticRequestDTO, services: ServiceContainer = Depends(get_services)):
    return services.water_service.statistic(water_statistic_dto, PeriodType.YEAR)


