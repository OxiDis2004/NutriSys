class User:
    def __init__(self):
        self._user_id = None
        self._telegram_id = None
        self._language = None
        self._name = None
        self._lastname = None
        self._birthday = None
        self._weight = None
        self._height = None
        self._sex = None

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
        self._weight = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def sex(self):
        return self._sex

    @sex.setter
    def sex(self, value):
        self._sex = value


