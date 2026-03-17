from fastapi import APIRouter, Depends

from src.dependencies import get_services, ServiceContainer
from src.models.dto.sent_food_request_dto import SentFoodRequestDTO
from src.models.dto.sent_food_response_dto import SentFoodResponseDTO
from src.models.dto.statistic_request_dto import StatisticRequestDTO
from src.models.property.period import PeriodType

router = APIRouter(prefix="/api/food")

@router.put("/add", response_model=SentFoodResponseDTO)
async def add_water(send_food_dto: SentFoodRequestDTO, services: ServiceContainer = Depends(get_services)):
    return services.food_service.sent_food(send_food_dto)

@router.post("/statistic/day", response_model=list[SentFoodResponseDTO])
async def statistic_week(statistic_dto: StatisticRequestDTO, services: ServiceContainer = Depends(get_services)):
    return services.food_service.statistic(statistic_dto, PeriodType.DAY)

@router.post("/statistic/week", response_model=list[SentFoodResponseDTO])
async def statistic_week(statistic_dto: StatisticRequestDTO, services: ServiceContainer = Depends(get_services)):
    return services.food_service.statistic(statistic_dto, PeriodType.WEEK)

@router.post("/statistic/month", response_model=list[SentFoodResponseDTO])
async def statistic_week(statistic_dto: StatisticRequestDTO, services: ServiceContainer = Depends(get_services)):
    return services.food_service.statistic(statistic_dto, PeriodType.MONTH)

@router.post("/statistic/year", response_model=list[SentFoodResponseDTO])
async def statistic_week(statistic_dto: StatisticRequestDTO, services: ServiceContainer = Depends(get_services)):
    return services.food_service.statistic(statistic_dto, PeriodType.YEAR)


