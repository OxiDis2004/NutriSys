import calendar
from collections import defaultdict
from datetime import date, datetime

from fastapi import HTTPException

from src.models.dto.water_request_dto import WaterRequestDTO
from src.models.dto.water_response_dto import WaterResponseDTO
from src.models.dto.water_statistic_request_dto import WaterStatisticRequestDTO
from src.models.property.period import Period
from src.services.db_service import DBService

class WaterService:
    def __init__(self, db_service: DBService):
        self._db_service = db_service

    def add_drunk_water(self, water_request: WaterRequestDTO) -> WaterResponseDTO:
        if water_request is None or water_request.user_id is None:
            raise HTTPException(status_code=400, detail="User id is null")

        try:
            today = date.today()
            rows = self._db_service.get_drunk_water(water_request.user_id, today)

            drunk_water = water_request.drunk_water
            if rows is None or rows.date is None:
                self._db_service.add_drunk_water(water_request.user_id, water_request.drunk_water,
                today)
            else:
                drunk_water += rows.water
                self._db_service.update_drunk_water(water_request.user_id,
                    drunk_water, today)

            return WaterResponseDTO(day=today, drunk_water_day=drunk_water)

        except Exception as e:
            raise HTTPException(status_code=400, detail="Caught " + str(e))

    def statistic(self, request: WaterStatisticRequestDTO) -> list[WaterResponseDTO]:
        if request.user_id is None:
            raise HTTPException(status_code=400, detail="User id is null")

        try:
            if request.day is not None:
                row = self._db_service.get_drunk_water(request.user_id, request.day)
                drunk_water = [WaterResponseDTO(day=row.date, drunk_water_day=row.water)]
                return drunk_water
            elif request.week is not None:
                rows = self.get_statistic_data(self.get_week, request.week, request.user_id)
            elif request.month is not None:
                rows = self.get_statistic_data(self.get_month, request.month, request.user_id)
            elif request.year is not None:
                rows = self.get_statistic_data(self.get_year, request.year, request.user_id)
                months = defaultdict(int)
                for row in rows:
                    key = f"{row.date.year}-{row.date.month}"
                    months[key] += row
                rows = months
            else:
                raise Exception("Date wouldn't be send")

            if len(rows) == 0:
                raise Exception("Nothing found")

            drunk_water: list[WaterResponseDTO] = []
            if isinstance(rows, defaultdict):
                for key, data in rows:
                    drunk_water.append(WaterResponseDTO(day=date.fromisoformat(key),
                        drunk_water_day=data))
            else:
                for row in rows:
                    drunk_water.append(WaterResponseDTO(day=row.date, drunk_water_day=row.water))

            return drunk_water
        except Exception as e:
            raise e

    def get_statistic_data(self, get_period_func, current_date: date | datetime, user_id: str ):
        period = get_period_func(current_date)
        period.start_date.isoformat()
        return self._db_service.get_drunk_water_interval(user_id, period)

    @staticmethod
    def get_week(week: date | datetime) -> Period:
        week_nr = week.isocalendar().week
        start = date.fromisocalendar(week.year, week_nr, 1)
        end = date.fromisocalendar(week.year, week_nr, 7)
        return Period(start, end)

    @staticmethod
    def get_month(month_date: date | datetime) -> Period:
        year, month = month_date.year, month_date.month
        week_day, days_in_month = calendar.monthrange(year, month)
        start = month_date.replace(day=1)
        end = month_date.replace(day=days_in_month)
        return Period(start, end)

    @staticmethod
    def get_year(year_date: date | datetime) -> Period:
        start = year_date.replace(month=1, day=1)
        end = year_date.replace(month=12, day=31)
        return Period(start, end)






