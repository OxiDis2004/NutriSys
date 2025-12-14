from fastapi import APIRouter, Depends

from src.dependencies import get_water_service
from src.models.dto.water_request_dto import WaterRequestDTO
from src.models.dto.water_response_dto import WaterResponseDTO
from src.models.dto.water_statistic_request_dto import WaterStatisticRequestDTO

router = APIRouter(prefix="/api/water")

@router.put("/add", response_model=WaterResponseDTO)
async def add_water(water_dto: WaterRequestDTO, service=Depends(get_water_service)):
    return service.add_drunk_water(water_dto)

@router.post("/statistic/day", response_model=list[WaterResponseDTO])
async def statistic_week(water_statistic_dto: WaterStatisticRequestDTO, service=Depends(
    get_water_service)):
    return service.statistic(water_statistic_dto)

@router.post("/statistic/week", response_model=list[WaterResponseDTO])
async def statistic_week(water_statistic_dto: WaterStatisticRequestDTO, service=Depends(
    get_water_service)):
    return service.statistic(water_statistic_dto)

@router.post("/statistic/month", response_model=list[WaterResponseDTO])
async def statistic_week(water_statistic_dto: WaterStatisticRequestDTO, service=Depends(
    get_water_service)):
    return service.statistic(water_statistic_dto)

@router.post("/statistic/year", response_model=list[WaterResponseDTO])
async def statistic_week(water_statistic_dto: WaterStatisticRequestDTO, service=Depends(
    get_water_service)):
    return service.statistic(water_statistic_dto)


