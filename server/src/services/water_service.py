import calendar
from datetime import date

from fastapi import HTTPException

from src.models.dto.water_request_dto import WaterRequestDTO
from src.models.dto.water_response_dto import WaterResponseDTO
from src.models.dto.water_statistic_request_dto import WaterStatisticRequestDTO
from src.models.property.period import Period, PeriodType
from src.services.db_service import DBService

class WaterService:
    def __init__(self, db_service: DBService):
        self._db_service = db_service

    def add_drunk_water(self, water_request: WaterRequestDTO) -> WaterResponseDTO:
        if water_request is None or water_request.user_id is None:
            raise HTTPException(status_code=400, detail="User id is null")

        try:
            today = date.today()
            result: list[WaterResponseDTO] = self.get_statistic_day(
                WaterStatisticRequestDTO(user_id=water_request.user_id, statistic_date=today)
            )
            drunk_water = water_request.drunk_water

            if result[0].drunk_water == 0:
                self._db_service.add_drunk_water(
                    water_request.user_id,
                    water_request.drunk_water,
                    today
                )
            else:
                drunk_water += result[0].drunk_water
                self._db_service.update_drunk_water(
                    water_request.user_id,
                    drunk_water,
                    today
                )

            return WaterResponseDTO(day=today.isoformat(), drunk_water=drunk_water)

        except Exception as e:
            raise HTTPException(status_code=500, detail="Caught " + str(e))

    def statistic(self, request: WaterStatisticRequestDTO, period_type_str: str) \
            -> list[WaterResponseDTO]:
        if request.user_id is None:
            raise HTTPException(status_code=400, detail="User id is null")

        try:
            period_type: PeriodType = PeriodType(period_type_str)
            match period_type:
                case PeriodType.DAY: return self.get_statistic_day(request)
                case PeriodType.WEEK: return self.get_statistic_week(request)
                case PeriodType.MONTH: return self.get_statistic_month(request)
                case PeriodType.YEAR: return self.get_statistic_year(request)

        except Exception as e:
            raise HTTPException(status_code=500, detail="Caught " + str(e))

    def get_statistic_day(self, request: WaterStatisticRequestDTO) -> list[WaterResponseDTO]:
        return self.get_statistic_data(self.get_day, request)

    def get_statistic_week(self, request: WaterStatisticRequestDTO) -> list[WaterResponseDTO]:
        return self.get_statistic_data(self.get_week, request)

    def get_statistic_month(self, request: WaterStatisticRequestDTO) -> list[WaterResponseDTO]:
        return self.get_statistic_data(self.get_month, request)

    def get_statistic_year(self, request: WaterStatisticRequestDTO) -> list[WaterResponseDTO]:
        return self.get_statistic_data(self.get_year, request, True)

    def get_statistic_data(self, period_func, request: WaterStatisticRequestDTO,
            step_month: bool = False):
        period = period_func(request.statistic_date)
        rows = self._db_service.get_drunk_water_interval(request.user_id, period)
        result = period.period_dict(step_month)

        for row in rows:
            key = row.date.isoformat() if not step_month \
                    else row.date.replace(day=1).isoformat()
            result[key] += row.water

        return [
            WaterResponseDTO(day=key, drunk_water=data) for key, data in result.items()
        ]

    @staticmethod
    def get_day(statistic_date: date) -> Period:
        return Period(statistic_date, statistic_date)

    @staticmethod
    def get_week(statistic_date: date) -> Period:
        week_nr = statistic_date.isocalendar().week
        start = date.fromisocalendar(statistic_date.year, week_nr, 1)
        end = date.fromisocalendar(statistic_date.year, week_nr, 7)
        return Period(start, end)

    @staticmethod
    def get_month(statistic_date: date) -> Period:
        year, month = statistic_date.year, statistic_date.month
        week_day, days_in_month = calendar.monthrange(year, month)
        start = statistic_date.replace(day=1)
        end = statistic_date.replace(day=days_in_month)
        return Period(start, end)

    @staticmethod
    def get_year(statistic_date: date) -> Period:
        start = statistic_date.replace(month=1, day=1)
        end = statistic_date.replace(month=12, day=31)
        return Period(start, end)
