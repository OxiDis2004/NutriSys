import datetime
from sqlalchemy import ForeignKey, DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.entity.base import Base

class SentFood(Base):
    __tablename__ = 'sent_food_from_user'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    food_id: Mapped[int] = mapped_column(ForeignKey("food.id"), nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(DATETIME, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="sent_food")
    food: Mapped["Food"] = relationship("Food", back_populates="sent_foods")

    def __repr__(self) -> str:
        return (f"Sent_food_from_user(id={self.id!r}, user_id={self.user_id!r}, "
                f"food_id={self.food_id!r}, date={self.date!r})")