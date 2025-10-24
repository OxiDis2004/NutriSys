from decimal import Decimal
from typing import List
from sqlalchemy import String, Integer, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.entity.base import Base


class Food(Base):
    __tablename__ = 'food'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    calory: Mapped[int] = mapped_column(Integer, nullable=False)
    protein: Mapped[Decimal] = mapped_column(DECIMAL(5,2), nullable=False)
    fat: Mapped[Decimal] = mapped_column(DECIMAL(5,2), nullable=False)
    carbon: Mapped[Decimal] = mapped_column(DECIMAL(5,2), nullable=False)

    sent_foods: Mapped[List["SentFood"]] = relationship(
        "SentFood", back_populates="food", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (f"Id(id={self.id!r}, name={self.name!r}, calory={self.calory!r},"
                f"protein={self.protein!r}, fat={self.fat!r}, carbon={self.carbon!r})")
