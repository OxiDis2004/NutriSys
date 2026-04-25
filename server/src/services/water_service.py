from datetime import date
from typing import Any, override
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import Row, Sequence

from src.models.dto.statistic_request_dto import StatisticRequestDTO
from src.models.dto.water_request_dto import WaterRequestDTO
from src.models.dto.water_response_dto import WaterResponseDTO
from src.models.property.period import Period, PeriodType
from src.services import StatisticService
from src.services.db_service import DBService


class WaterService(StatisticService):
    def __init__(self, db_service: DBService):
        super().__init__(db_service)

    def add_drunk_water(self, water_request: WaterRequestDTO) -> WaterResponseDTO:
        if water_request is None or water_request.user_id is None:
            raise HTTPException(status_code=400, detail="User id is null")

        try:
            today = date.today()
            request = StatisticRequestDTO(
                user_id=water_request.user_id, statistic_date=today
            )
            result: list[WaterResponseDTO] = self.statistic(request, PeriodType.DAY)
            drunk_water = water_request.drunk_water

            if result[0].drunk_water == 0:
                self._db_service.add_drunk_water(
                    water_request.user_id, water_request.drunk_water, today
                )
            else:
                drunk_water += result[0].drunk_water
                self._db_service.update_drunk_water(
                    water_request.user_id, drunk_water, today
                )

            return WaterResponseDTO(day=today.isoformat(), drunk_water=drunk_water)

        except Exception as err:
            raise HTTPException(status_code=500, detail="Caught " + str(err)) from err

    @override
    def _default_dict_value(self):
        return 0

    @override
    def _update_dict_value(self, dict_value: Any, new_value: Any) -> Any:
        return dict_value + new_value.water

    @override
    def _get_data_from_db(self, user_id: UUID, period: Period) -> Sequence[Row[Any]]:
        return self._db_service.get_drunk_water_interval(user_id, period)

    @override
    def _wrap_func(self, result: dict) -> list[WaterResponseDTO]:
        return [
            WaterResponseDTO(day=key, drunk_water=data) for key, data in result.items()
        ]
