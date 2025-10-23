from datetime import datetime
from sqlalchemy import String, ForeignKey, DATETIME
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

from language import Language


class User(DeclarativeBase):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    language_id: Mapped[int] = mapped_column(ForeignKey("language.id"), nullable=False)
    last_activity: Mapped[datetime] = mapped_column(DATETIME, nullable=False)

    language: Mapped["Language"] = relationship(back_populates="users")

    def __repr__(self) -> str:
        lang = self.language.iso if self.language else 'uk'
        return (
            f"User(id={self.id!r}, name={self.name!r}, "
            f"language={lang!r}, last_activity={self.last_activity!r})"
        )