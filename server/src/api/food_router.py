from fastapi import APIRouter, Depends

from src.dependencies import ServiceContainer, get_services
from src.models.dto.food_record_request_dto import FoodRecordRequestDTO
from src.models.dto.food_record_response_dto import FoodRecordResponseDTO
from src.models.dto.statistic_request_dto import StatisticRequestDTO
from src.models.property.period import PeriodType

router = APIRouter(prefix="/api/food")


@router.put("/add", response_model=list[FoodRecordResponseDTO])
async def add_food(
        send_food_dto: FoodRecordRequestDTO,
        services: ServiceContainer = Depends(get_services),  # noqa: B008
):
    """Process a sent food image and return nutrition information.

    Args:
        send_food_dto (FoodRecordRequestDTO): Request containing the food image.
        services (ServiceContainer): Application service container.

    Returns:
        FoodRecordResponseDTO: Recognized food and nutrition data.
    """

    return services.food_service.add_food_record(send_food_dto)


@router.post("/statistic/{period}", response_model=list[FoodRecordResponseDTO])
async def statistic_food(
        period: PeriodType,
        statistic_dto: StatisticRequestDTO,
        services: ServiceContainer = Depends(get_services),  # noqa: B008
):
    """Return food consumption statistics for a selected period.

    Args:
        period (PeriodType): Statistic aggregation period.
        statistic_dto (StatisticRequestDTO): Statistic request data.
        services (ServiceContainer): Application service container.

    Returns:
        list[FoodRecordResponseDTO]: Food statistics grouped by date.
    """

    return services.food_service.statistic(statistic_dto, period)
