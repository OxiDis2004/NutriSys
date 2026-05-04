import logging
import uuid
from datetime import date, datetime

from fastapi import HTTPException, status
from fastapi.responses import Response

from src.models.dto.user_dto import UserDTO
from src.models.dto.user_info_dto import UserInfoDTO
from src.models.property.activity import Activity
from src.models.property.goal import Goal
from src.services.db_service import DBService

logger = logging.getLogger(__name__)

class UserService:
    """Service responsible for user management operations.

    Handles user-related business logic including retrieval, creation,
    updating and authentication-related data access.
    """

    def __init__(self, db_service: DBService):
        self._db_service: DBService = db_service

    def login(self, user: UserDTO) -> UserDTO:
        """Authenticate an existing user by Telegram identifier.

        Args:
            user (UserDTO): Login request data.

        Returns:
            UserDTO: User data with internal id and language.

        Raises:
            HTTPException: If the request is invalid, the user is not found or
            activity update fails.
        """

        logger.debug("Login request started for telegram_id=%s", user.telegram_id)

        if user.telegram_id is None:
            logger.warning("Login failed: telegram_id is missing")
            raise HTTPException(status_code=422, detail="Unprocessable Entity")

        data = self._db_service.get_user(user.telegram_id)

        if data is None or data.id is None:
            logger.warning("Login failed: user not found, telegram_id=%s", user.telegram_id)
            raise HTTPException(status_code=404, detail="User not found")

        user.id = data.id
        user.language = data.iso if user.language is None else user.language

        try:
            self._db_service.update_user_activity(user.id)
            logger.info("User logged in successfully, user_id=%s", user.id)
            return user
        except Exception as err:
            logger.exception("Login failed while updating user activity, user_id=%s", user.id)
            raise HTTPException(status_code=400, detail="Caught: " + str(err)) from err

    def register(self, user: UserDTO) -> UserDTO:
        """Register a new user.

        Args:
            user (UserDTO): User registration data.

        Returns:
            UserDTO: Created user data with internal id.

        Raises:
            HTTPException: If the user already exists or cannot be created.
        """

        user.id = uuid.uuid4()
        logger.debug("Register request started for telegram_id=%s", user.telegram_id)

        if user.telegram_id is None:
            logger.warning("Register failed: telegram_id is missing")
            raise HTTPException(status_code=422, detail="User cannot be created")

        data = self._db_service.get_user(user.telegram_id)
        if data is not None:
            logger.warning("Register failed: user already exists, telegram_id=%s", user.telegram_id)
            raise HTTPException(
                status_code=400,
                detail={ "message": "User already exists" }
            )

        try:
            self._db_service.add_user(user, datetime.now())
            data = self._db_service.get_user(user.telegram_id)
        except Exception as err:
            logger.exception(
                "Register failed while creating user, telegram_id=%s", user.telegram_id
            )
            raise HTTPException(status_code=500, detail="Caught: " + str(err)) from err

        if data is None:
            logger.error("Register failed: user was not created, telegram_id=%s", user.telegram_id)
            raise HTTPException(status_code=500, detail="User couldn't create")

        user.id = data.id
        logger.info(
            "User registered successfully, user_id=%s, telegram_id=%s", user.id, user.telegram_id
        )
        return user

    def get_information(self, user: UserDTO) -> UserInfoDTO:
        """Return profile information for a user.

        Args:
            user (UserDTO): User identifier data.

        Returns:
            UserInfoDTO: User profile information.

        Raises:
            HTTPException: If user id is missing or profile information is not found.
        """

        logger.debug("Get user information request started, user_id=%s", user.id)

        if user.id is None:
            logger.warning("Get information failed: user_id is missing")
            raise HTTPException(status_code=422, detail="User id is undefined")

        data = self._db_service.get_user_info(user.id)
        if data is None:
            logger.warning(
                "Get information failed: user information not found, user_id=%s", user.id
            )
            raise HTTPException(status_code=404, detail="User information not found")

        logger.info("User information received successfully, user_id=%s", user.id)
        return UserInfoDTO(**data._mapping)

    def update_information(self, user_info: UserInfoDTO):
        """Update profile information for a user.

        Args:
            user_info (UserInfoDTO): New profile information.

        Returns:
            Response: HTTP 202 response if the update is successful.

        Raises:
            HTTPException: If user id is missing or update fails.
        """

        logger.debug("Update user information request started, user_id=%s", user_info.id)

        if user_info.id is None:
            logger.warning("Update information failed: user_id is missing")
            raise HTTPException(status_code=422, detail="User id is undefined")

        try:
            user = self._db_service.get_user_info(user_info.id)
            if user is None:
                logger.warning(
                    "Update information failed: user not found, user_id=%s", user_info.id
                )
                raise Exception("User couldn't update")

            self._db_service.update_user_info(user_info)
            logger.info("User information updated successfully, user_id=%s", user_info.id)
            return Response(status_code=status.HTTP_202_ACCEPTED)
        except Exception as err:
            logger.exception("Update information failed, user_id=%s", user_info.id)
            raise HTTPException(status_code=500, detail="Caught: " + str(err)) from err

    def update_language(self, user: UserDTO):
        """Update the selected language for a user.

        Args:
            user (UserDTO): User data containing id and language.

        Returns:
            Response: HTTP 202 response if the update is successful.

        Raises:
            HTTPException: If user data is invalid or update fails.
        """

        logger.debug("Update language request started, user_id=%s", user.id)

        if user.user_id is None:
            logger.warning("Update language failed: user details not found, user_id=%s", user.id)
            raise HTTPException(status_code=422, detail="User details not found")

        try:
            self._db_service.update_user_language(user)
            self._db_service.update_user_activity(user.id)

            logger.info("User language updated successfully, user_id=%s", user.id)
            return Response(status_code=status.HTTP_202_ACCEPTED)

        except Exception as err:
            logger.exception("Update language failed, user_id=%s", user.id)
            raise HTTPException(status_code=400, detail="Caught: " + str(err)) from err

    def calculate_bmr(self, user: UserDTO) -> dict[str, int]:
        """Calculate the user's recommended calorie norm.

        Uses stored profile information, age, sex, weight, height, activity level
        and goal to calculate the final BMR-based recommendation.

        Args:
            user (UserDTO): User identifier data.

        Returns:
            dict[str, int]: Dictionary with calculated BMR value.

        Raises:
            HTTPException: If required profile data is missing or invalid.
        """

        logger.debug("Calculate BMR request started, user_id=%s", user.id)

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
            logger.warning("BMR calculation failed: missing required data, user_id=%s", user.id)
            raise HTTPException(
                status_code=422,
                detail="Not all the necessary data has been entered."
            )

        year = self.years_old(user_info.birthday)
        if year == -1:
            logger.warning("BMR calculation failed: birthday is in the future, user_id=%s", user.id)
            raise HTTPException(
                status_code=400,
                detail="The birthday must be smaller than today."
            )

        bmr = self.formula(user_info.weight, user_info.height, year, user_info.sex)
        logger.debug("Base BMR calculated, user_id=%s, bmr=%s", user.id, bmr)

        if isinstance(user_info.activity, Activity):
            bmr = self.set_bmr_by_activity(bmr, user_info.activity)
            logger.debug(
                "BMR adjusted by activity, user_id=%s, activity=%s, bmr=%s",
                user.id,
                user_info.activity,
                bmr
            )

        if isinstance(user_info.goal, Goal):
            bmr = self.set_bmr_by_goal(bmr, user_info.goal)
            logger.debug(
                "BMR adjusted by goal, user_id=%s, goal=%s, bmr=%s",
                user.id,
                user_info.goal,
                bmr
            )

        result = round(bmr)
        logger.info("BMR calculated successfully, user_id=%s, bmr=%s", user.id, result)

        return { "bmr": result }

    def years_old(self, birthday: date) -> int:
        """Calculate age from birthday.

        Args:
            birthday (date): User birthday.

        Returns:
            int: User age in years, or -1 if birthday is in the future.
        """

        today = self.get_today()
        if birthday > today:
            return -1

        year = today.year - birthday.year
        if birthday.month > today.month or birthday.day > today.day:
            year -= 1

        return year

    @staticmethod
    def get_today():
        """Return the current date.

        Returns:
            date: Current local date.
        """
        return date.today()

    @staticmethod
    def formula(weight: int, height: int, years: int, sex: str) -> float:
        """Calculate base BMR using weight, height, age and sex.

        Args:
            weight (int): User weight in kilograms.
            height (int): User height in centimeters.
            years (int): User age in years.
            sex (str): User sex code.

        Returns:
            float: Calculated base BMR value.
        """

        return (
                (10 * weight)
                + (6.25 * height)
                - (5 * years)
                + (5 if sex == "m" else (-161))
        )

    @staticmethod
    def set_bmr_by_activity(normal_bmr: float, activity: Activity) -> float:
        """Adjust BMR according to activity level.

        Args:
            normal_bmr (float): Base BMR value.
            activity (Activity): User activity level.

        Returns:
            float: Activity-adjusted BMR value.
        """

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
        """Adjust BMR according to the user's nutrition goal.

        Args:
            normal_bmr (float): Current BMR value.
            goal (Goal): User nutrition goal.

        Returns:
            float: Goal-adjusted BMR value.
        """

        match goal:
            case Goal.LoseWeight:
                return normal_bmr * 0.9
            case Goal.MaintainWeight:
                return normal_bmr
            case Goal.GainWeight:
                return normal_bmr * 1.1
