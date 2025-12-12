import datetime
import uuid

import pytest

from src.models.dto.user_dto import UserDTO
from src.models.dto.user_info_dto import UserInfoDTO
from src.models.property.activity import Activity
from src.models.property.goal import Goal
from src.services.user_service import UserService
from fastapi import HTTPException

class TestUserService:

    @pytest.fixture(autouse=True)
    def setup_mocks(self, mocker):
        self.db_service_mock = mocker.Mock()
        self.user_service_mock = UserService(self.db_service_mock)

    def test_login_successful(self, mocker):
        telegram_id = "example_id"
        user = UserDTO(telegram_id=telegram_id)
        received_user = mocker.Mock()
        received_user.id = str(uuid.uuid4())
        received_user.iso = 'ua'
        self.db_service_mock.get_user.return_value = received_user

        user = self.user_service_mock.login(user)

        assert user.id == received_user.id
        assert user.telegram_id == telegram_id
        assert user.language == received_user.iso
        self.db_service_mock.get_user.assert_called_once_with(telegram_id)
        self.db_service_mock.update_user_activity.assert_called_once_with(telegram_id)

    def test_login_failed(self, mocker):
        telegram_id = "example_id"
        user = UserDTO(telegram_id=telegram_id)
        received_user = None
        self.db_service_mock.get_user.return_value = received_user

        with pytest.raises(Exception) as e_info:
            self.user_service_mock.login(user)

        assert e_info.errisinstance(HTTPException) == True
        code, detail = str(e_info.value).split(": ")
        assert code == '404'
        assert detail == "User not found"

    def test_register_successful(self, mocker):
        telegram_id = "example_id"
        user = UserDTO(telegram_id=telegram_id, language='ua')
        received_user = mocker.Mock()
        received_user.id = str(uuid.uuid4())
        received_user.iso = 'ua'
        self.db_service_mock.get_user.side_effect = [None, received_user]

        user = self.user_service_mock.register(user)

        assert user.id == received_user.id
        assert user.telegram_id == telegram_id
        assert user.language == received_user.iso
        assert self.db_service_mock.get_user.call_count == 2

    def test_register_user_exists(self, mocker):
        telegram_id = "example_id"
        user = UserDTO(telegram_id=telegram_id, language='ua')
        received_user = mocker.Mock()
        received_user.id = str(uuid.uuid4())
        received_user.iso = 'ua'
        self.db_service_mock.get_user.return_value = received_user

        with pytest.raises(Exception) as e_info:
            user = self.user_service_mock.register(user)

        assert e_info.errisinstance(HTTPException) == True
        code, detail = str(e_info.value).split(": ")
        assert code == '400'
        assert detail == "User exists"
        assert self.db_service_mock.get_user.call_count == 1

    def test_register_user_null_failed(self, mocker):
        user = UserDTO(telegram_id=None, language=None)

        with pytest.raises(Exception) as e_info:
            self.user_service_mock.register(user)

        assert e_info.errisinstance(HTTPException) == True
        code, detail = str(e_info.value).split(": ")
        assert code == '400'
        assert detail == "User cannot be created"

    def test_not_registered(self, mocker):
        telegram_id = "example_id"
        user = UserDTO(telegram_id=telegram_id, language='ua')
        received_user = None
        self.db_service_mock.get_user.return_value = received_user

        with pytest.raises(Exception) as e_info:
            self.user_service_mock.register(user)

        assert e_info.errisinstance(HTTPException) == True
        code, detail = str(e_info.value).split(": ")
        assert code == '404'
        assert detail == "User couldn't create"

    def test_update_information(self, mocker):
        user_info = UserInfoDTO(id=str(uuid.uuid4()), name='Denys', lastname='Ponomarenko')

        self.user_service_mock.update_information(user_info)

        self.db_service_mock.update_user_info.assert_called_once_with(user_info)

    def test_update_information_failed(self, mocker):
        user_info = UserInfoDTO(id=None)

        with pytest.raises(Exception) as e_info:
            self.user_service_mock.update_information(user_info)

        assert e_info.errisinstance(HTTPException) == True
        code, detail = str(e_info.value).split(": ")
        assert code == '400'
        assert detail == "User id is undefined"

    def test_calculate_calorie_successful(self, mocker):
        user_info = UserInfoDTO(
            id=str(uuid.uuid4()),
            name='Denys',
            lastname='Ponomarenko',
            birthday=datetime.date.fromisocalendar(2005, 1, 4),
            weight=105,
            height=181,
            sex='m',
            count_of_sport_in_week=Activity.HighActivity,
            goal=Goal.LoseWeight
        )
        self.user_service_mock.years_old = mocker.Mock(return_value=20)
        self.user_service_mock.formula = mocker.Mock(return_value=2000)
        self.user_service_mock.set_bmr_by_activity = mocker.Mock(return_value=3000)
        self.user_service_mock.set_bmr_by_goal = mocker.Mock(return_value=2700)

        response = self.user_service_mock.calculate_calorie(user_info)

        assert response['bmr'] == 2700
        self.user_service_mock.years_old.assert_called_once_with(user_info.birthday)
        self.user_service_mock.formula.assert_called_once_with(
            user_info.weight,
            user_info.height,
            20,
            user_info.sex
        )
        self.user_service_mock.set_bmr_by_activity.assert_called_once_with(
            2000,
            user_info.count_of_sport_in_week
        )
        self.user_service_mock.set_bmr_by_goal.assert_called_once_with(
            3000,
            user_info.goal
        )

    def test_calculate_calorie_failed(self, mocker):
        user_info = UserInfoDTO(
            id=None,
            name='Denys',
            lastname='Ponomarenko',
        )

        response = self.user_service_mock.calculate_calorie(user_info)

        assert response['bmr'] == 0

    def test_years_old_normal(self, mocker):
        today = datetime.date(2025, 5, 6)
        birthday = datetime.date.fromisocalendar(2005, 1, 4)
        self.user_service_mock.get_today = mocker.Mock(return_value=today)

        year = self.user_service_mock.years_old(birthday)

        assert year == 20

    def test_years_old_month_bigger(self, mocker):
        today = datetime.date.today()
        today = today.replace(today.year, 10, today.day)
        birthday = today.replace(2005, today.month + 1, today.day)
        self.user_service_mock.get_today = mocker.Mock(return_value=today)

        year = self.user_service_mock.years_old(birthday)

        assert year == 19

    def test_years_old_day_bigger(self, mocker):
        today = datetime.date.today()
        today = today.replace(today.year, today.month, 25)
        birthday = today.replace(2005, today.month, today.day + 2)
        self.user_service_mock.get_today = mocker.Mock(return_value=today)

        year = self.user_service_mock.years_old(birthday)

        assert year == 19

    def test_birthday_bigger_for_today(self, mocker):
        today = datetime.date.today().replace(2025, 12, 10)
        birthday = today.replace(today.year, today.month, today.day + 1)
        self.user_service_mock.get_today = mocker.Mock(return_value=today)

        year = self.user_service_mock.years_old(birthday)

        assert year == -1