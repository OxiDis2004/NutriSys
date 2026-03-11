from collections import defaultdict
from datetime import date, timedelta
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

    def period_dict(self, step_month: bool = False) -> dict[str, int]:
        result = defaultdict(int)
        current = self._start_date

        while current <= self._end_date:
            key = current.isoformat()
            result[key] = 0

            if step_month:
                if current.month == 12:
                    break
                current = current.replace(month=current.month + 1)
            else:
                current += timedelta(days=1)

        return result

class PeriodType(Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"