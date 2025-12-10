from datetime import datetime

from sqlalchemy import ForeignKey, String, DATETIME, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.models.entity.base import Base


class UserInfo(Base):
    __tablename__ = "user_info"

    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"), primary_key=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(55), nullable=True)
    lastname: Mapped[str] = mapped_column(String(55), nullable=True)
    birthday: Mapped[datetime] = mapped_column(DATETIME, nullable=True)
    weight: Mapped[int] = mapped_column(Integer, nullable=True)
    height: Mapped[int] = mapped_column(Integer, nullable=True)
    sex: Mapped[str] = mapped_column(String(2), nullable=True)
    count_of_sport_in_week: Mapped[int] = mapped_column(Integer, nullable=True)
    goal: Mapped[int] = mapped_column(Integer, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="info")

    def __repr__(self) -> str:
        return (
            f"UserInfo("
            f"user_id={self.user_id!r}, "
            f"name={self.name!r}, "
            f"lastname={self.lastname!r}, "
            f"birthday={self.birthday!r}, "
            f"weight={self.weight!r}, "
            f"height={self.height!r}, "
            f"sex={self.sex!r}, "
            f"count_of_sport_in_week={self.count_of_sport_in_week!r}, "
            f"goal={self.goal!r}"
            f")"
        )