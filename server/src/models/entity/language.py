from typing import List
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

from src.models.entity.user import User


class Language(DeclarativeBase):
    __tablename__ = 'language'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    iso: Mapped[str] = mapped_column(String(3), nullable=False)

    users: Mapped[List["User"]] = relationship(
        back_populates="language", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Language(id={self.id!r}, iso={self.iso!r})"