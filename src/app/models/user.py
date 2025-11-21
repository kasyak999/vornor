from sqlalchemy import BigInteger
from app.core.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    """Модель пользователя."""

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        unique=True,
        comment='Телеграм id',
    )
    is_superuser: Mapped[bool] = mapped_column(
        default=False,
        comment='Статус суперпользователя',
    )
    password: Mapped[str] = mapped_column(
        nullable=True,
        comment='Хеш пароля',
    )
    api_key: Mapped[str] = mapped_column(
        nullable=True,
        comment='API key от биржи',
    )
    api_secret: Mapped[str] = mapped_column(
        nullable=True,
        comment='API secret от биржи',
    )
    demo: Mapped[bool] = mapped_column(
        nullable=True,
        comment='Использование демо счета',
    )
    coins: Mapped[list["Coin"]] = relationship(
        "Coin",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    coin_slots: Mapped[list["CoinSlot"]] = relationship(
        "CoinSlot",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f'{self.telegram_id}'
