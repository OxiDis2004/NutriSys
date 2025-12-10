import datetime
from decimal import Decimal
from sqlalchemy import DECIMAL, ForeignKey, DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.entity.base import Base

class DrunkWater(Base):
    __tablename__ = 'drunk_water'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"), nullable=False)
    water: Mapped[Decimal] = mapped_column(DECIMAL(5, 2), nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(DATETIME, nullable=False)

    user: Mapped["User"] = relationship(
        "User", back_populates="drunk_water"
    )

    def __repr__(self) -> str:
        return (f"Drunk_water(id={self.id!r}, user_id={self.user_id!r}, "
                f"water={self.water!r}, date={self.date!r})")