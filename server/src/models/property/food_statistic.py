from decimal import Decimal
from dataclasses import dataclass


@dataclass
class FoodStatistic:
    _name: str = None
    _calorie: int = None
    _protein: Decimal = None
    _carbon: Decimal = None
    _fat: Decimal = None

    def update(self, value: "FoodStatistic") -> "FoodStatistic":
        self._calorie += value._calorie if value._calorie is not None else 0
        self._protein += value._protein if value._protein is not None else Decimal(0)
        self._carbon += value._carbon if value._carbon is not None else Decimal(0)
        self._fat += value._fat if value._fat is not None else Decimal(0)
        return self

    def from_row(self, row):
        self._name=row.name,
        self._calorie=row.calory,
        self._protein=row.protein,
        self._carbon=row.carbon,
        self._fat=row.fat

    @property
    def name(self):
        return self._name if self._name is not None else ''

    @property
    def calorie(self):
        return self._calorie if self._calorie is not None else 0

    @property
    def protein(self):
        return self._protein if self._protein is not None else Decimal(0)

    @property
    def carbon(self):
        return self._carbon if self._carbon is not None else Decimal(0)

    @property
    def fat(self):
        return self._fat if self._fat is not None else Decimal(0)
