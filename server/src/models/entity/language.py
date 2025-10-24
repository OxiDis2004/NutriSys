from typing import List
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.models.entity.base import Base


class Language(Base):
    __tablename__ = 'language'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    iso: Mapped[str] = mapped_column(String(3), nullable=False)

    users: Mapped[List["User"]] = relationship(
        "User", back_populates="language", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Language(id={self.id!r}, iso={self.iso!r})"