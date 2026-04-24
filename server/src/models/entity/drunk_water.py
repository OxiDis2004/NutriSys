import datetime
from sqlalchemy import ForeignKey, DATE, INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.entity.base import Base

class DrunkWater(Base):
    __tablename__ = 'drunk_water'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"), nullable=False)
    water: Mapped[int] = mapped_column(INTEGER, nullable=False)
    date: Mapped[datetime.date] = mapped_column(DATE, nullable=False)

    user: Mapped["User"] = relationship(
        "User", back_populates="drunk_water"
    )

    def __repr__(self) -> str:
        return (f"Drunk_water(id={self.id!r}, user_id={self.user_id!r}, "
                f"water={self.water!r}, date={self.date!r})")