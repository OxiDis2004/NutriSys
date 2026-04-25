from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.entity.base import Base

LANGUAGE_ISO = ["ua", "en", "de"]


class Language(Base):
    __tablename__ = "language"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    iso: Mapped[str] = mapped_column(String(3), nullable=False)

    users: Mapped[list["User"]] = relationship(
        "User", back_populates="language", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Language(id={self.id!r}, iso={self.iso!r})"
