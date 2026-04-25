import uuid
from datetime import date, datetime

from fastapi import HTTPException, status
from fastapi.responses import Response

from src.models.dto.user_dto import UserDTO
from src.models.dto.user_info_dto import UserInfoDTO
from src.models.property.activity import Activity
from src.models.property.goal import Goal
from src.services.db_service import DBService


class UserService:
    def __init__(self, db_service: DBService):
        self._db_service: DBService = db_service

    def login(self, user: UserDTO) -> UserDTO:
        if user.telegram_id is None:
            raise HTTPException(status_code=422, detail="Unprocessable Entity")

        data = self._db_service.get_user(user.telegram_id)

        if data is None or data.id is None:
            raise HTTPException(status_code=404, detail="User not found")

        user.id = data.id
        user.language = data.iso if user.language is None else user.language

        try:
            self._db_service.update_user_activity(user.id)
            return user
        except Exception as err:
            raise HTTPException(status_code=400, detail="Caught: " + str(err)) from err

    def register(self, user: UserDTO) -> UserDTO:
        user.id = uuid.uuid4()

        if user.id is None or user.telegram_id is None or user.language is None:
            raise HTTPException(status_code=422, detail="User cannot be created")

        user_last_activity = datetime.now()

        data = self._db_service.get_user(user.telegram_id)
        if data is not None:
            raise HTTPException(
                status_code=400, detail={ "message": "User already exists" }
            )

        self._db_service.add_user(user, user_last_activity)
        data = self._db_service.get_user(user.telegram_id)

        if data is None:
            raise HTTPException(status_code=500, detail="User couldn't create")

        user.id = data.id
        return user

    def get_information(self, user: UserDTO) -> UserInfoDTO:
        if user.id is None:
            raise HTTPException(status_code=422, detail="User id is undefined")

        data = self._db_service.get_user_info(user.id)
        if data is None:
            raise HTTPException(status_code=404, detail="User information not found")

        user_info = UserInfoDTO(**data._mapping)
        return user_info

    def update_information(self, user_info: UserInfoDTO):
        if user_info.id is None:
            raise HTTPException(status_code=422, detail="User id is undefined")

        try:
            user = self._db_service.get_user_info(user_info.id)
            if user is None:
                raise Exception("User couldn't update")

            self._db_service.update_user_info(user_info)
            return Response(status_code=status.HTTP_202_ACCEPTED)
        except Exception as err:
            raise HTTPException(status_code=500, detail="Caught: " + str(err)) from err

    def update_language(self, user: UserDTO):
        if user.user_id is None:
            raise HTTPException(status_code=422, detail="User details not found")

        try:
            self._db_service.update_user_language(user)
            self._db_service.update_user_activity(user.id)
            return Response(status_code=status.HTTP_202_ACCEPTED)
        except Exception as err:
            raise HTTPException(status_code=400, detail="Caught: " + str(err)) from err

    def calculate_bmr(self, user: UserDTO) -> dict[str, int]:
        user_info = self.get_information(user)

        if (
                user_info.weight is None
                or not isinstance(user_info.weight, int)
                or user_info.height is None
                or not isinstance(user_info.height, int)
                or user_info.birthday is None
                or not isinstance(user_info.birthday, date)
                or user_info.sex is None
                or not isinstance(user_info.sex, str)
        ):
            raise HTTPException(
                status_code=422, detail="Not all the necessary data has been entered."
            )

        year = self.years_old(user_info.birthday)
        if year == -1:
            raise HTTPException(
                status_code=400, detail="The birthday must be smaller than today."
            )

        bmr = self.formula(user_info.weight, user_info.height, year, user_info.sex)

        if isinstance(user_info.activity, Activity):
            bmr = self.set_bmr_by_activity(bmr, user_info.activity)

        if isinstance(user_info.goal, Goal):
            bmr = self.set_bmr_by_goal(bmr, user_info.goal)

        return { "bmr": round(bmr) }

    def years_old(self, birthday: date) -> int:
        today = self.get_today()
        if birthday > today:
            return -1

        year = today.year - birthday.year
        if birthday.month > today.month or birthday.day > today.day:
            year -= 1

        return year

    @staticmethod
    def get_today():
        return date.today()

    @staticmethod
    def formula(weight: int, height: int, years: int, sex: str) -> float:
        return (
                (10 * weight)
                + (6.25 * height)
                - (5 * years)
                + (5 if sex == "m" else (-161))
        )

    @staticmethod
    def set_bmr_by_activity(normal_bmr: float, activity: Activity) -> float:
        match activity:
            case Activity.NoActivity:
                return normal_bmr
            case Activity.LowActivity:
                return normal_bmr * 1.1
            case Activity.MiddleActivity:
                return normal_bmr * 1.3
            case Activity.HighActivity:
                return normal_bmr * 1.5
            case Activity.HighestActivity:
                return normal_bmr * 1.7

    @staticmethod
    def set_bmr_by_goal(normal_bmr: float, goal: Goal) -> float:
        match goal:
            case Goal.LoseWeight:
                return normal_bmr * 0.9
            case Goal.MaintainWeight:
                return normal_bmr
            case Goal.GainWeight:
                return normal_bmr * 1.1
