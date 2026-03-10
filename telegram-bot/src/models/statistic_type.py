from enum import Enum


class StatisticType(Enum):
    WATER = "water_statistic"
    CALORIE = "calorie_statistic"
    DAY = "statistic/day"
    WEEK = "statistic/week"
    MONTH = "statistic/month"
    YEAR = "statistic/year"