from datetime import date
from enum import Enum


class Period:
    def __init__(self, start_date, end_date):
        self._start_date: date = start_date
        self._end_date: date = end_date

    @property
    def start_date(self):
        return self._start_date.isoformat()

    @property
    def end_date(self):
        return self._end_date.isoformat()

class PeriodType(Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"