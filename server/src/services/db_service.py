from datetime import date, datetime
import os
from uuid import UUID

from sqlalchemy import Engine, update, select, Row, delete, text, func
from sqlalchemy.dialects.postgresql import insert

from src.models.adapter.database_adapter import DBAdapter
from src.models.dto.nutrient_food_dto import NutrientFoodDTO
from src.models.dto.user_dto import UserDTO
from src.models.dto.user_info_dto import UserInfoDTO
from src.models.entity.drunk_water import DrunkWater
from src.models.entity.food import Food
from src.models.entity.language import Language, LANGUAGE_ISO
from src.models.entity.sent_food import SentFood
from src.models.entity.user import User
from src.models.entity.user_info import UserInfo
from src.models.property.period import Period


class DBService:
    def __init__(self, engine: Engine):
        self.db = DBAdapter(engine)
        self.db.init_db()

    def get_users(self):
        stmt = (
            select(User.id.label("id"),  Language.iso.label("iso"))
            .join(User.language)
        )
        return self.db.fetch(stmt)

    def get_user(self, telegram_id: int) -> Row:
        stmt = (select(User.id.label("id"), Language.iso.label("iso"))
                .join(User.language)
                .where(User.telegram_id == telegram_id))
        return self.db.fetch_one(stmt)

    def add_user(self, user: UserDTO, activity: datetime):
        stmt = insert(User).values([
            {
                "id": user.user_id,
                "telegram_id": user.telegram_id,
                "language_id": select(Language.id).where(Language.iso == user.language),
                "last_activity": activity
            }
        ])

        self.db.commit(stmt)

        stmt = insert(UserInfo).values([ { "user_id": user.user_id } ])
        self.db.commit(stmt)

    def initialize_languages(self):
        isos = [row.iso for row in self.get_languages()]

        for iso in LANGUAGE_ISO:
            if iso not in isos:
                self.add_language(iso)

    def update_user_language(self, user: UserDTO):
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

    def update_user_activity(self, user_id: UUID):
        user_last_activity = datetime.now()

        stmt = (
            update(User)
            .where(User.id == str(user_id))
            .values(last_activity=user_last_activity)
        )

        self.db.commit(stmt)

    def get_user_infos(self, user_ids: list[UUID]):
        stmt = (
            select(
                UserInfo.name.label("name"),
                UserInfo.lastname.label("lastname"),
                UserInfo.birthday.label("birthday"),
                UserInfo.weight.label("weight"),
                UserInfo.height.label("height"),
                UserInfo.count_of_sport_in_week.label("activity"),
                UserInfo.goal.label("goal")
            )
            .where(UserInfo.user_id.in_([str(user_id) for user_id in user_ids]))
        )
        return self.db.fetch(stmt)

    def get_user_info(self, user_id: UUID):
        stmt = (
            select(
                UserInfo.name.label("name"),
                UserInfo.lastname.label("lastname"),
                UserInfo.birthday.label("birthday"),
                UserInfo.weight.label("weight"),
                UserInfo.height.label("height"),
                UserInfo.count_of_sport_in_week.label("activity"),
                UserInfo.goal.label("goal")
            )
            .where(UserInfo.user_id == str(user_id))
        )
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
                count_of_sport_in_week=user.count_of_sport_in_week.value,
                goal=user.goal.value
            )
        )

        self.db.commit(stmt)

    def get_drunk_water_interval(self, user_id: UUID, period: Period):
        stmt = (
            select(DrunkWater.date.label("date"), func.sum(DrunkWater.water).label("water"))
            .where(DrunkWater.user_id == str(user_id))
            .where(DrunkWater.date >= period.start_date)
            .where(DrunkWater.date <= period.end_date)
            .group_by(DrunkWater.date)
        )

        return self.db.fetch(stmt)

    def add_drunk_water(self, user_id: UUID, drunk_water: int, _date: date):
        stmt = insert(DrunkWater).values(user_id=str(user_id), water=drunk_water, date=_date)
        self.db.commit(stmt)

    def update_drunk_water(self, user_id: UUID, drunk_water: int, _date: date):
        stmt = (
            update(DrunkWater)
            .where(DrunkWater.user_id == str(user_id))
            .where(DrunkWater.date == _date)
            .values(water=drunk_water)
        )
        self.db.commit(stmt)

    def get_sent_food(self, user_id: UUID, search_date: datetime):
        stmt = (
            select(SentFood.date.label("date"), SentFood.food_id.label("food"),
                SentFood.image_id.label("image"))
            .where(SentFood.user_id == str(user_id))
            .where(SentFood.date == search_date)
            .group_by(SentFood.date)
        )

        return self.db.fetch(stmt)

    def get_sent_food_interval(self, user_id: UUID, date_from: date, date_to: date):
        stmt = (
            select(SentFood.date.label("date"), SentFood.food_id.label("food"),
                SentFood.image_id.label("image"))
            .where(SentFood.user_id == str(user_id))
            .where(SentFood.date > date_from)
            .where(SentFood.date < date_to)
            .group_by(SentFood.date)
        )

        return self.db.fetch(stmt)

    def add_sent_food(self, user_id: UUID, food_id: str, image_id: str | None):
        date_now = date.today()

        stmt = (
            insert(SentFood).values([
                {
                    "user_id": str(user_id),
                    "food_id": food_id,
                    "image_id": image_id,
                    "date": date_now
                }
            ])
        )

        self.db.commit(stmt)

    def get_nutrient(self, food_id: str):
        stmt = (
            select(Food.calory.label("calory"), Food.protein.label("protein"),
                Food.carbon.label("carbon"), Food.fat.label("fat"))
                .where(Food.id == food_id)
        )

        return self.db.fetch(stmt)

    def get_nutrient_by_name(self, food_name: str):
        stmt = (
            select(
                Food.id.label("id"), Food.calory.label("calory"),
                Food.protein.label("protein"), Food.carbon.label("carbon"), Food.fat.label("fat"))
            .where(Food.name == food_name)
        )

        return self.db.fetch(stmt)

    def add_food(self, food_id: str, food_dto: NutrientFoodDTO):
        stmt = (
            insert(Food).values([
                {
                    "id": food_id,
                    "name": food_dto.name,
                    "calory": food_dto.calorie,
                    "protein": food_dto.protein,
                    "fat": food_dto.fat,
                    "carbon": food_dto.carbon
                }
            ])
        )

        self.db.commit(stmt)

    #-------- FOR TESTS --------
    def check_health(self):
        stmt = select(text("1"))
        return len(self.db.fetch(stmt)) > 0

    def delete_user(self, telegram_id: int):
        stmt = delete(User).where(User.telegram_id == telegram_id)
        self.db.commit(stmt)

    def delete_drunk_water(self, user_id: UUID):
        stmt = delete(DrunkWater).where(DrunkWater.user_id == str(user_id))
        self.db.commit(stmt)

    def get_languages(self):
        stmt = select(Language.iso.label("iso"))
        return self.db.fetch(stmt)

    def add_language(self, iso: str):
        insert_stmt = insert(Language).values(iso=iso)
        self.db.commit(insert_stmt)

    def close_session(self):
        self.db.close_session()

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
