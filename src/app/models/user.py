from sqlalchemy import Integer
from app.core.db import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    """Модель пользователя."""

    telegram_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        unique=True,
        comment='Название монеты',
    )

    def __repr__(self) -> str:
        return f'{self.telegram_id}'
