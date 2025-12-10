from datetime import date, datetime
import os
import uuid

from sqlalchemy import Engine, update, select, Row
from sqlalchemy.dialects.mysql import insert

from src.models.adapter.database_adapter import DBAdapter
from src.models.dto.user_dto import UserDTO
from src.models.dto.user_info_dto import UserInfoDTO
from src.models.entity.drunk_water import DrunkWater
from src.models.entity.food import Food
from src.models.entity.language import Language
from src.models.entity.sent_food import SentFood
from src.models.entity.user import User
from src.models.entity.user_info import UserInfo


class DBService:
    def __init__(self, engine: Engine):
        self.db = DBAdapter(engine)
        self.db.init_db()

    def get_user(self, telegram_id: str) -> Row:
        stmt = (select(User.id.label("id"), Language.iso.label("iso"))
                .join(User.language)
                .where(User.telegram_id == telegram_id))
        return self.db.fetch_one(stmt)

    def add_user(self, user: UserDTO, activity: datetime):
        stmt = insert(User).values([
            {
                "id": user.id,
                "telegram_id": user.telegram_id,
                "language_id": select(Language.id).where(Language.iso == user.language),
                "last_activity": activity
            }
        ])

        self.db.commit(stmt)

        stmt = insert(UserInfo).values([ { "user_id": user.id } ])
        self.db.commit(stmt)

    def update_user_activity(self, user_id: str):
        user_last_activity = datetime.now()

        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(last_activity=user_last_activity)
        )

        self.db.commit(stmt)

    def update_user_info(self, user: UserInfoDTO):
        stmt = (
            update(UserInfo)
            .where(UserInfo.user_id == user.id)
            .values(
                name=user.name,
                lastname=user.lastname,
                birthday=user.birthday,
                weight=user.weight,
                height=user.height,
                sex=user.sex,
                count_of_sport_in_week=user.count_of_sport_in_week.value,
                goal=user.goal.value
            )
        )

        self.db.commit(stmt)

    def get_drunk_water(self, user_id: str, search_date: date):
        stmt = (
            select(DrunkWater.date, DrunkWater.water)
            .where(DrunkWater.user_id == user_id)
            .where(DrunkWater.date == search_date)
            .group_by(DrunkWater.date)
        )

        return self.db.fetch(stmt)

    def get_drunk_water_interval(self, user_id: str, date_from: date, date_to: date):
        stmt = (
            select(DrunkWater.date, DrunkWater.water)
            .where(DrunkWater.user_id == user_id)
            .where(DrunkWater.date > date_from)
            .where(DrunkWater.date < date_to)
            .group_by(DrunkWater.date)
        )

        return self.db.fetch(stmt)

    def insert_drunk_water(self, user_id: str, drunk_water: int):
        date_now = date.today()

        stmt = (
            insert(DrunkWater).values([
                {
                    "user_id": user_id,
                    "water": drunk_water,
                    "date": date_now
                }
            ])
        )

        self.db.commit(stmt)

    def get_sent_food(self, user_id: str, search_date: date):
        stmt = (
            select(SentFood.date, SentFood.food_id, SentFood.image_id)
            .where(SentFood.user_id == user_id)
            .where(SentFood.date == search_date)
            .group_by(SentFood.date)
        )

        return self.db.fetch(stmt)

    def get_sent_food_interval(self, user_id: str, date_from: date, date_to: date):
        stmt = (
            select(SentFood.date, SentFood.food_id, SentFood.image_id)
            .where(SentFood.user_id == user_id)
            .where(SentFood.date > date_from)
            .where(SentFood.date < date_to)
            .group_by(SentFood.date)
        )

        return self.db.fetch(stmt)

    def insert_sent_food(self, user_id: str, food_id: str, image_id: str | None):
        date_now = date.today()

        stmt = (
            insert(SentFood).values([
                {
                    "user_id": user_id,
                    "food_id": food_id,
                    "image_id": image_id,
                    "date": date_now
                }
            ])
        )

        self.db.commit(stmt)

    def get_food(self, food_id: str):
        stmt = (
            select(Food.id, Food.name, Food.calory,
                      Food.protein, Food.carbon, Food.fat)
                .where(Food.id == food_id)
        )

        return self.db.fetch(stmt)

    @staticmethod
    def get_db_host():
        return os.getenv('DB_HOST')

    @staticmethod
    def get_db_port():
        return os.getenv('DB_PORT')

    @staticmethod
    def get_db_user():
        return os.getenv('DB_USER')

    @staticmethod
    def get_db_pwd():
        return os.getenv('DB_PASSWORD')

    @staticmethod
    def get_db_database():
        return os.getenv('DB_DATABASE')
