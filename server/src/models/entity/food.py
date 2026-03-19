from decimal import Decimal
from typing import List
from sqlalchemy import String, Integer, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.entity.base import Base


class Food(Base):
    __tablename__ = 'food'

    id: Mapped[str] = mapped_column(String(40), primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    calorie: Mapped[int] = mapped_column(Integer, nullable=False)
    protein: Mapped[Decimal] = mapped_column(DECIMAL(6,2), nullable=False)
    carbon: Mapped[Decimal] = mapped_column(DECIMAL(6,2), nullable=False)
    fat: Mapped[Decimal] = mapped_column(DECIMAL(6,2), nullable=False)

    sent_foods: Mapped[List["SentFood"]] = relationship(
        "SentFood", back_populates="food", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (f"Id("
                f"id={self.id!r}, "
                f"name={self.name!r}, "
                f"calory={self.calorie!r},"
                f"protein={self.protein!r}, "
                f"fat={self.fat!r}, "
                f"carbon={self.carbon!r}"
                f")")
