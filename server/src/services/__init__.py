import calendar
from abc import ABC, abstractmethod
from datetime import date
from typing import Any
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import Row, Sequence

from src.models.dto.statistic_request_dto import StatisticRequestDTO
from src.models.property.period import Period, PeriodType


class StatisticService(ABC):
    """Abstract base class for statistic aggregation services.

    Provides common logic for grouping statistic data by day, week, month or
    year. Subclasses define how raw database rows are loaded, accumulated and
    converted into response DTOs.
    """

    def __init__(self, db_service):
        """Initialize statistic service.

        Args:
            db_service: Database service used to load statistic data.
        """
        self._db_service = db_service

    @abstractmethod
    def _wrap_func[T](self, result: dict) -> list[T]:
        pass

    @abstractmethod
    def _get_data_from_db(self, user_id: UUID, period: Period) -> Sequence[Row[Any]]:
        pass

    @abstractmethod
    def _update_dict_value(self, dict_value: Any, new_value: Any) -> Any:
        pass

    @abstractmethod
    def _default_dict_value(self):
        pass

    def statistic[T](
            self, request: StatisticRequestDTO, period_type: PeriodType
    ) -> list[T]:
        """Calculate statistics for the selected period type.

        Args:
            request (StatisticRequestDTO): Statistic request data.
            period_type (PeriodType): Period type used for aggregation.

        Returns:
            list[T]: Statistic response objects.

        Raises:
            HTTPException: If the request is invalid or statistic calculation fails.
        """

        if request.user_id is None:
            raise HTTPException(status_code=400, detail="User id is null")

        try:
            result = None

            match period_type:
                case PeriodType.DAY:
                    result = self.get_statistic_day(request)
                case PeriodType.WEEK:
                    result = self.get_statistic_week(request)
                case PeriodType.MONTH:
                    result = self.get_statistic_month(request)
                case PeriodType.YEAR:
                    result = self.get_statistic_year(request)
            if result is None:
                return []

            return self._wrap_func(result)

        except Exception as err:
            raise HTTPException(status_code=500, detail="Caught " + str(err)) from err

    def get_statistic_day(self, request: StatisticRequestDTO) -> dict:
        """Calculate statistics for one day.

        Args:
            request (StatisticRequestDTO): Statistic request data.

        Returns:
            dict: Aggregated daily statistic data.
        """

        return self.get_statistic_data(self.get_day, request)

    def get_statistic_week(self, request: StatisticRequestDTO) -> dict:
        """Calculate statistics for one week.

        Args:
           request (StatisticRequestDTO): Statistic request data.

        Returns:
           dict: Aggregated weekly statistic data.
        """

        return self.get_statistic_data(self.get_week, request)

    def get_statistic_month(self, request: StatisticRequestDTO) -> dict:
        """Calculate statistics for one month.

        Args:
            request (StatisticRequestDTO): Statistic request data.

        Returns:
            dict: Aggregated monthly statistic data.
        """

        return self.get_statistic_data(self.get_month, request)

    def get_statistic_year(self, request: StatisticRequestDTO) -> dict:
        """Calculate statistics for one year.

        Args:
            request (StatisticRequestDTO): Statistic request data.

        Returns:
            dict: Aggregated yearly statistic data grouped by month.
        """
        return self.get_statistic_data(self.get_year, request, True)

    def get_statistic_data(
            self, period_func, request: StatisticRequestDTO, step_month: bool = False
    ) -> dict:
        """Load and aggregate statistic data for a calculated period.

        Args:
            period_func: Function that converts a date into a Period object.
            request (StatisticRequestDTO): Statistic request data.
            step_month (bool): Whether to group result keys by month.

        Returns:
            dict: Aggregated statistic values indexed by date string.
        """

        period: Period = period_func(request.statistic_date)
        rows = self._get_data_from_db(request.user_id, period)
        result = period.period_dict(self._default_dict_value(), step_month)

        for row in rows:
            key = (
                row.date.isoformat()
                if not step_month
                else row.date.replace(day=1).isoformat()
            )
            result[key] = self._update_dict_value(result[key], row)

        return result

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
