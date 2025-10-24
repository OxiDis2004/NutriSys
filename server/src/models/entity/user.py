from datetime import datetime
from sqlalchemy import String, ForeignKey, DATETIME
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.models.entity.base import Base
from src.models.entity.drunk_water import DrunkWater


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    language_id: Mapped[int] = mapped_column(ForeignKey("language.id"), nullable=False)
    last_activity: Mapped[datetime] = mapped_column(DATETIME, nullable=False)

    language: Mapped["Language"] = relationship("Language", back_populates="users")

    drunk_water: Mapped["DrunkWater"] = relationship(
        "DrunkWater", back_populates="user", cascade="all, delete-orphan"
    )

    sent_food: Mapped["SentFood"] = relationship(
        "SentFood", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        lang = self.language.iso if self.language else 'uk'
        return (
            f"User(id={self.id!r}, name={self.name!r}, "
            f"language={lang!r}, last_activity={self.last_activity!r})"
        )