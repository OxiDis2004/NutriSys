from datetime import date

from src.models.activity import Activity
from src.models.goal import Goal
from src.models.language import Language
from src.models.sex import Sex


class User:
    def __init__(self, user_id = None, telegram_id = None, language: Language = Language.ENGLISH):
        self._user_id: str = user_id
        self._telegram_id: int = telegram_id
        self._language: Language = language
        self._name: str = None
        self._lastname: str = None
        self._birthday: date = None
        self._weight: int = None
        self._height: int = None
        self._sex: Sex = None
        self._activity: Activity = None
        self._goal: Goal = None

    def __str__(self):
        return (f"ID: {self._user_id}"
                f"TelegramID: {self._telegram_id}")

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def telegram_id(self):
        return self._telegram_id

    @telegram_id.setter
    def telegram_id(self, value):
        self._telegram_id = value

    @property
    def language(self):
        return self._language.value if self._language is not None else None

    @language.setter
    def language(self, value: str):
        self._language = self.parse_data(value, Language, Language.ENGLISH)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def lastname(self):
        return self._lastname

    @lastname.setter
    def lastname(self, value):
        self._lastname = value

    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthday(self, value):
        self._birthday = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = self.parse_data(value, int)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = self.parse_data(value, int)

    @property
    def sex(self):
        return self._sex.value if self._sex is not None else None

    @sex.setter
    def sex(self, value):
        self._sex = self.parse_data(value, Sex)

    @property
    def activity(self):
        return self._activity if self._activity is not None else None

    @activity.setter
    def activity(self, value):
        self._activity = self.parse_data(value, Activity)

    @property
    def goal(self):
        return self._goal if self._goal is not None else None

    @goal.setter
    def goal(self, value):
        self._goal = self.parse_data(value, Goal)

    def base_info(self):
        return {
            "id": self._user_id,
            "telegram_id": self._telegram_id,
            "language": self._language.value
        }

    @staticmethod
    def parse_data(value, parse_func, default = None):
        try:
            return parse_func(value) if value is not None else default
        except (KeyError, ValueError):
            return None