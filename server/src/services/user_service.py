import uuid
from datetime import date, datetime
from fastapi import HTTPException

from src.services.db_service import DBService
from src.models.dto.user_dto import UserDTO
from src.models.dto.user_info_dto import UserInfoDTO
from src.models.property.activity import Activity
from src.models.property.goal import Goal


class UserService:
    def __init__(self, db_service: DBService):
        self.db_service: DBService = db_service

    def login(self, user: UserDTO) -> UserDTO:
        data = self.db_service.get_user(user.telegram_id)

        if data is None or data.id is None:
            raise HTTPException(status_code=404, detail="User not found")

        user.id = data.id
        user.language = data.iso if user.language is None else user.language

        self.db_service.update_user_activity(user.telegram_id)
        return user

    def register(self, user: UserDTO) -> UserDTO:
        user.id = str(uuid.uuid4())

        if user.id is None or user.telegram_id is None or user.language is None:
            raise HTTPException(status_code=400, detail="User cannot be created")

        user_last_activity = datetime.now()
        self.db_service.add_user(user, user_last_activity)
        data = self.db_service.get_user(user.telegram_id)

        if data is None:
            raise HTTPException(status_code=404, detail="User couldn't create")

        user.id = data.id
        return user

    def update_information(self, user_info: UserInfoDTO):
        if user_info.id is None:
            raise HTTPException(status_code=400, detail="User id is undefined")

        self.db_service.update_user_info(user_info)

    def calculate_calorie(self, user_info: UserInfoDTO) -> int:
        if user_info.weight is None or \
            user_info.height is None or \
            user_info.birthday is None or \
            user_info.sex is None:
            return 0

        year = self.years_old(user_info.birthday)
        bmr = self.formula(user_info.weight, user_info.height, year, user_info.sex)

        if isinstance(user_info.count_of_sport_in_week, Activity):
            bmr = self.set_bmr_by_activity(bmr, user_info.count_of_sport_in_week)

        if isinstance(user_info.goal, Goal):
            bmr = self.set_bmr_by_goal(bmr, user_info.goal)

        return round(bmr)

    def years_old(self, birthday: date) -> int:
        today = self.get_today()
        if birthday > today:
            return -1

        year = today.year - birthday.year
        if birthday.month > today.month:
            year -= 1
        elif birthday.day > today.day:
            year -= 1

        return year

    @staticmethod
    def get_today():
        return date.today()

    @staticmethod
    def formula(weight: int, height: int, years: int, sex: str) -> float:
        return (10 * weight) + (6.25 * height) - (5 * years) + (5 if sex == 'm' else (-161))

    @staticmethod
    def set_bmr_by_activity(normal_bmr: float, activity: Activity) -> float:
        match activity:
            case Activity.NoActivity: return normal_bmr
            case Activity.LowActivity: return normal_bmr * 1.1
            case Activity.MiddleActivity: return normal_bmr * 1.3
            case Activity.HighActivity: return normal_bmr * 1.5
            case Activity.HighestActivity: return normal_bmr * 1.7

    @staticmethod
    def set_bmr_by_goal(normal_bmr: float, goal: Goal) -> float:
        match goal:
            case Goal.LoseWeight: return normal_bmr * 0.9
            case Goal.MaintainWeight: return normal_bmr
            case Goal.GainWeight: return normal_bmr * 1.1