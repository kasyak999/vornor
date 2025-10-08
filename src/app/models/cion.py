from sqlalchemy import String, Float, Boolean, ForeignKey, Integer
from app.core.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint


class Coin(Base):
    """Модель монеты для торговли."""

    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='uq_user_coin_name'),
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment='Название монеты',
    )
    buy_usdt: Mapped[str] = mapped_column(
        String(50),
        nullable=True,
        comment='На сколько USDT покупать монету если стоит в цикле',
    )
    cycle: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment='Зацикливание монеты true / false на покупку и продажу',
    )
    price_buy: Mapped[float] = mapped_column(
        Float,
        nullable=True,
        comment='Курс первой покупки монеты',
    )
    last_price_buy: Mapped[float] = mapped_column(
        Float,
        nullable=True,
        comment='Курс последней покупки монеты',
    )
    order_buy_id: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
        comment='ID ордера на покупку',
    )
    order_sell_id: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
        comment='ID ордера на продажу',
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id', ondelete='CASCADE', name='fk_coin_user_id'),
        nullable=False,
        comment='ID пользователя',
    )
    user: Mapped["User"] = relationship("User", back_populates="coins")

    def __repr__(self) -> str:
        return f'{self.name}'
