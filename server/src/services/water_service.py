from collections import defaultdict
from datetime import date

from fastapi import HTTPException

from src.models.dto.water_request_dto import WaterRequestDTO
from src.models.dto.water_response_dto import WaterResponseDTO
from src.models.dto.water_statistic_request_dto import WaterStatisticRequestDTO
from src.services.db_service import DBService




class WaterService:
    def __init__(self, db_service: DBService):
        self._db_service = db_service

    def add_drunk_water(self, water_request: WaterRequestDTO):
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

            return WaterResponseDTO(drunk_water_day=drunk_water)

        except Exception as e:
            raise HTTPException(status_code=400, detail="Caught " + str(e))

    def statistic(self, request: WaterStatisticRequestDTO):
        if request.user_id is None:
            raise HTTPException(status_code=400, detail="User id is null")

        try:
            if request.day is not None:
                row = self._db_service.get_drunk_water(
                    request.user_id, request.day
                )
                drunk_water = { row.date.isoformat(): int(row.water) }
                return drunk_water
            elif request.week is not None:
                monday, sunday = self.get_week(request.week)
                rows = self._db_service.get_drunk_water_interval(
                    request.user_id, monday, sunday
                )
            elif request.month is not None:
                start_month, end_month = self.get_month(request.month)
                rows = self._db_service.get_drunk_water_interval(
                    request.user_id, start_month, end_month
                )
            elif request.year is not None:
                start_year = request.year.replace(request.year.year, 1, 1)
                end_year = request.year.replace(request.year.year, 12, 31)
                rows = self._db_service.get_drunk_water_interval(
                    request.user_id, start_year, end_year
                )
            else:
                raise Exception("Date wouldn't be send")

            if len(rows) == 0:
                raise Exception("Nothing found")

            drunk_water = defaultdict(int)
            for row in rows:
                drunk_water[row.date.isoformat()] += int(row.water)

            return drunk_water
        except Exception as e:
            raise e



    def get_week(self, week: date):
        global monday, sunday
        day = week.day
        day_of_week = week.weekday()

        match day_of_week:
            case 0: monday, sunday = day, day + 6
            case 1: monday, sunday = day + 1, day + 5
            case 2: monday, sunday = day + 2, day + 4
            case 3: monday, sunday = day + 3, day + 3
            case 4: monday, sunday = day + 4, day + 2
            case 5: monday, sunday = day + 5, day + 1
            case 6: monday, sunday = day + 6, day
            case _: monday, sunday = 1, 7

        return (week.replace(week.year, week.month, monday),
                week.replace(week.year, week.month, sunday))

    def get_month(self, month_date: date):
        global start, end
        year, month = month_date.year, month_date.month
        start = month_date.replace(year, month, 1)

        if month in [1, 3, 5, 7, 8, 10, 12]:
            day = 31
        elif month == 2:
            day = 29 if (year % 4 == 0 or year % 100 == 0) and year % 400 == 0 else 28
        else:
            day = 30

        end = month_date.replace(year, month, day)
        return start, end





