from fastapi import APIRouter, Depends

from src.dependencies import ServiceContainer, get_services
from src.models.dto.statistic_request_dto import StatisticRequestDTO
from src.models.dto.water_request_dto import WaterRequestDTO
from src.models.dto.water_response_dto import WaterResponseDTO
from src.models.property.period import PeriodType

router = APIRouter(prefix="/api/water")


@router.put("/add", response_model=WaterResponseDTO)
async def add_water(
        water_dto: WaterRequestDTO,
        services: ServiceContainer = Depends(get_services),  # noqa: B008
):
    return services.water_service.add_drunk_water(water_dto)


@router.post("/statistic/{period}", response_model=list[WaterResponseDTO])
async def statistic_water(
        period: PeriodType,
        statistic_dto: StatisticRequestDTO,
        services: ServiceContainer = Depends(get_services),  # noqa: B008
):
    return services.water_service.statistic(statistic_dto, period)
