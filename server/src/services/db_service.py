import os
from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Engine, Row, delete, func, select, text, update
from sqlalchemy.dialects.postgresql import insert

from src.models.adapter.database_adapter import DBAdapter
from src.models.dto.user_dto import UserDTO
from src.models.dto.user_info_dto import UserInfoDTO
from src.models.entity.drunk_water import DrunkWater
from src.models.entity.food import Food
from src.models.entity.language import LANGUAGE_ISO, Language
from src.models.entity.sent_food import SentFood
from src.models.entity.user import User
from src.models.entity.user_info import UserInfo
from src.models.property.food_statistic import FoodStatistic
from src.models.property.period import Period


class DBService:
    """Service for database access operations.

    Provides methods for user, profile, language, water, food and statistic
    persistence. SQLAlchemy statements are created here and executed through
    DBAdapter.
    """

    def __init__(self, engine: Engine):
        """Initialize database service and database schema.

        Args:
            engine (Engine): SQLAlchemy engine connected to the application database.
        """
        self.db = DBAdapter(engine)
        self.db.init_db()

    def get_user(self, telegram_id: int) -> Row:
        """Return a user by Telegram identifier.

        Args:
            telegram_id (int): Telegram user identifier.

        Returns:
            Row: Row containing user id and language ISO code.
        """

        stmt = (
            select(User.id.label("id"), Language.iso.label("iso"))
            .join(User.language)
            .where(User.telegram_id == telegram_id)
        )
        return self.db.fetch_one(stmt)

    def get_user_by_id(self, user_id: UUID) -> Row:
        stmt = (
            select(User.id.label("id"), Language.iso.label("iso"))
            .join(User.language)
            .where(User.id == str(user_id))
        )
        return self.db.fetch_one(stmt)

    def add_user(self, user: UserDTO, activity: datetime):
        """Create a user and related empty profile record.

        Args:
            user (UserDTO): User data to insert.
            activity (datetime): Initial last activity timestamp.
        """

        stmt = insert(User).values(
            [
                {
                    "id": user.user_id,
                    "telegram_id": user.telegram_id,
                    "language_id": select(Language.id).where(
                        Language.iso == user.language
                    ),
                    "last_activity": activity,
                }
            ]
        )

        self.db.commit(stmt)

        stmt = insert(UserInfo).values([{ "user_id": user.user_id }])
        self.db.commit(stmt)

    def initialize_languages(self):
        """Ensure that all supported language ISO codes exist in the database."""

        isos = [row.iso for row in self.get_languages()]

        for iso in LANGUAGE_ISO:
            if iso not in isos:
                self.add_language(iso)

    def update_user_language(self, user: UserDTO):
        """Update the selected language of a user.

        Args:
            user (UserDTO): User data containing user id and language code.
        """

        stmt = (
            update(User)
            .where(User.id == user.user_id)
            .values(
                language_id=(
                    select(Language.id)
                    .where(Language.iso == user.language)
                    .scalar_subquery()
                )
            )
        )
        self.db.commit(stmt)

    def update_user_activity(self, user_id: UUID | None):
        user_last_activity = datetime.now()

        stmt = (
            update(User)
            .where(User.id == str(user_id))
            .values(last_activity=user_last_activity)
        )

        self.db.commit(stmt)

    def get_user_infos(self, user_ids: list[UUID]):
        """Return profile information for multiple users.

        Args:
            user_ids (list[UUID]): List of internal user identifiers.

        Returns:
            Sequence[Row]: User profile rows.
        """

        stmt = select(
            UserInfo.name.label("name"),
            UserInfo.lastname.label("lastname"),
            UserInfo.birthday.label("birthday"),
            UserInfo.weight.label("weight"),
            UserInfo.height.label("height"),
            UserInfo.activity.label("activity"),
            UserInfo.goal.label("goal"),
        ).where(UserInfo.user_id.in_([str(user_id) for user_id in user_ids]))
        return self.db.fetch(stmt)

    def get_user_info(self, user_id: UUID):
        """Return detailed profile information for one user.

        Args:
            user_id (UUID): Internal user identifier.

        Returns:
            Row: User profile row.
        """

        stmt = select(
            UserInfo.user_id.label("id"),
            UserInfo.name.label("name"),
            UserInfo.lastname.label("lastname"),
            UserInfo.birthday.label("birthday"),
            UserInfo.weight.label("weight"),
            UserInfo.height.label("height"),
            UserInfo.sex.label("sex"),
            UserInfo.activity.label("activity"),
            UserInfo.goal.label("goal"),
        ).where(UserInfo.user_id == str(user_id))
        return self.db.fetch_one(stmt)

    def update_user_info(self, user: UserInfoDTO):
        stmt = (
            update(UserInfo)
            .where(UserInfo.user_id == user.user_id)
            .values(
                name=user.name,
                lastname=user.lastname,
                birthday=user.birthday,
                weight=user.weight,
                height=user.height,
                sex=user.sex,
                activity=user.activity,
                goal=user.goal,
            )
        )
        self.db.commit(stmt)

    def get_drunk_water_interval(self, user_id: UUID, period: Period):
        """Return water consumption grouped by date for a period.

        Args:
            user_id (UUID): Internal user identifier.
            period (Period): Requested date interval.

        Returns:
            Sequence[Row]: Rows containing date and total water amount.
        """

        stmt = (
            select(
                DrunkWater.date.label("date"), func.sum(DrunkWater.water).label("water")
            )
            .where(DrunkWater.user_id == str(user_id))
            .where(DrunkWater.date >= period.start_date)
            .where(DrunkWater.date <= period.end_date)
            .group_by(DrunkWater.date)
        )

        return self.db.fetch(stmt)

    def add_drunk_water(self, user_id: UUID, drunk_water: int, _date: date):
        """Insert water consumption for a date.

        Args:
            user_id (UUID): Internal user identifier.
            drunk_water (int): Consumed water amount.
            _date (date): Consumption date.
        """

        stmt = insert(DrunkWater).values(
            user_id=str(user_id), water=drunk_water, date=_date
        )
        self.db.commit(stmt)

    def update_drunk_water(self, user_id: UUID, drunk_water: int, _date: date):
        """Update water consumption for a date.

        Args:
            user_id (UUID): Internal user identifier.
            drunk_water (int): Updated consumed water amount.
            _date (date): Consumption date.
        """

        stmt = (
            update(DrunkWater)
            .where(DrunkWater.user_id == str(user_id))
            .where(DrunkWater.date == _date)
            .values(water=drunk_water)
        )
        self.db.commit(stmt)

    def get_sent_food_images(self, user_id: UUID, period: Period):
        """Return distinct food image identifiers sent by a user.

        Args:
            user_id (UUID): Internal user identifier.
            period (Period): Requested date interval.

        Returns:
            Sequence[Row]: Rows containing image identifiers.
        """

        stmt = (
            select(SentFood.image_id.label("image"))
            .where(SentFood.user_id == str(user_id))
            .where(SentFood.date >= period.start_date)
            .where(SentFood.date <= period.end_date)
            .distinct()
        )
        return self.db.fetch(stmt)

    def get_sent_food(self, user_id: UUID, period: Period):
        """Return aggregated food nutrient statistics for a period.

        Args:
            user_id (UUID): Internal user identifier.
            period (Period): Requested date interval.

        Returns:
            Sequence[Row]: Rows containing date, food name and nutrient sums.
        """

        stmt = (
            select(
                SentFood.date.label("date"),
                Food.name.label("name"),
                func.sum(Food.calorie * SentFood.weight / 100).label("calorie"),
                func.sum(Food.protein * SentFood.weight / 100).label("protein"),
                func.sum(Food.carbon * SentFood.weight / 100).label("carbon"),
                func.sum(Food.fat * SentFood.weight / 100).label("fat"),
            )
            .join(SentFood.food)
            .where(SentFood.user_id == str(user_id))
            .where(SentFood.date >= period.start_date)
            .where(SentFood.date <= period.end_date)
            .group_by(SentFood.date)
        )

        return self.db.fetch(stmt)

    def update_sent_food(self, user_id: UUID):
        """Reset today's sent food weight for a user.

        Args:
            user_id (UUID): Internal user identifier.
        """

        curr_day = date.today()
        stmt = (
            update(SentFood)
            .where(SentFood.user_id == str(user_id))
            .where(SentFood.date == curr_day)
            .values(weight=0)
        )
        self.db.commit(stmt)

    def add_sent_food(self, user_id: UUID, food_id: str, image_id: str, weight: int):
        """Insert a recognized food entry sent by a user.

        Args:
            user_id (UUID): Internal user identifier.
            food_id (str): Food identifier.
            image_id (str): Uploaded image identifier.
            weight (int): Estimated food weight.
        """

        date_now = date.today()

        stmt = insert(SentFood).values(
            [
                {
                    "user_id": str(user_id),
                    "food_id": food_id,
                    "image_id": image_id,
                    "date": date_now,
                    "weight": weight,
                }
            ]
        )

        self.db.commit(stmt)

    def get_food_by_id(self, food_id: str):
        """Return food data by identifier.

        Args:
            food_id (str): Food identifier.

        Returns:
            Sequence[Row]: Matching food rows.
        """

        return self.get_food(Food.id == food_id)

    def get_food_by_name(self, food_name: str):
        """Return food data by name.

        Args:
            food_name (str): Food name.

        Returns:
            Sequence[Row]: Matching food rows.
        """

        return self.get_food(Food.name == food_name)

    def get_food(self, condition):
        """Return food records matching a SQLAlchemy condition.

        Args:
            condition: SQLAlchemy filter condition.

        Returns:
            Sequence[Row]: Matching food rows.
        """

        stmt = select(
            Food.id.label("_id"),
            Food.name.label("_name"),
            Food.calorie.label("_calorie"),
            Food.protein.label("_protein"),
            Food.carbon.label("_carbon"),
            Food.fat.label("_fat"),
        ).where(condition)

        return self.db.fetch(stmt)

    def add_food(self, food_id: str, food: FoodStatistic):
        """Insert a new food record with nutrient values.

        Args:
            food_id (str): Food identifier.
            food (FoodStatistic): Food nutrient information.
        """

        stmt = insert(Food).values(
            [
                {
                    "id": food_id,
                    "name": food.name,
                    "calorie": food.calorie,
                    "protein": food.protein,
                    "fat": food.fat,
                    "carbon": food.carbon,
                }
            ]
        )

        self.db.commit(stmt)

    # -------- FOR TESTS --------
    def check_health(self):
        """Check whether the database connection is available.

        Returns:
            bool: True if the database responds successfully.
        """

        stmt = select(text("1"))
        return len(self.db.fetch(stmt)) > 0

    def delete_user(self, telegram_id: int):
        """Delete a user by Telegram identifier.

        Args:
            telegram_id (int): Telegram user identifier.
        """

        stmt = delete(User).where(User.telegram_id == telegram_id)
        self.db.commit(stmt)

    def delete_drunk_water(self, user_id: UUID):
        """Delete all water records for a user.

        Args:
            user_id (UUID): Internal user identifier.
        """

        stmt = delete(DrunkWater).where(DrunkWater.user_id == str(user_id))
        self.db.commit(stmt)

    def get_languages(self):
        """Return all supported language ISO codes.

        Returns:
            Sequence[Row]: Rows containing language ISO codes.
        """

        stmt = select(Language.iso.label("iso"))
        return self.db.fetch(stmt)

    def add_language(self, iso: str):
        """Insert a supported language ISO code.

        Args:
            iso (str): Language ISO code.
        """

        insert_stmt = insert(Language).values(iso=iso)
        self.db.commit(insert_stmt)

    def close_session(self):
        """Close the underlying database session."""
        self.db.close_session()

    @staticmethod
    def get_db_host():
        return os.getenv("DB_HOST")

    @staticmethod
    def get_db_port():
        return os.getenv("DB_PORT")

    @staticmethod
    def get_db_user():
        return os.getenv("DB_USER")

    @staticmethod
    def get_db_pwd():
        return os.getenv("DB_PASSWORD")

    @staticmethod
    def get_db_database():
        return os.getenv("DB_DATABASE")
