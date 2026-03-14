from src.models.activity import Activity
from src.models.goal import Goal
from src.models.sex import Sex


class User:
    def __init__(self, user_id, telegram_id, language):
        self._user_id = user_id
        self._telegram_id = telegram_id
        self._language = language
        self._name = None
        self._lastname = None
        self._birthday = None
        self._weight = None
        self._height = None
        self._sex = None
        self._activity = None
        self._goal = None

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
        return self._language

    @language.setter
    def language(self, value):
        self._language = value

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
        return self._sex

    @sex.setter
    def sex(self, value):
        self._sex = self.parse_data(value, Sex)

    @property
    def activity(self):
        return self._activity

    @activity.setter
    def activity(self, value):
        self._activity = self.parse_data(value, Activity)

    @property
    def goal(self):
        return self._goal

    @goal.setter
    def goal(self, value):
        self._goal = self.parse_data(value, Goal)

    @staticmethod
    def parse_data(value, parse_func):
        try:
            return parse_func(value) if value is not None else None
        except (KeyError, ValueError):
            return None