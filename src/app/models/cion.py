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
    buy_usdt: Mapped[Float] = mapped_column(
        Float,
        nullable=True,
        comment='На сколько USDT покупать монету если стоит в цикле',
        default=5.5
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
    count_buy: Mapped[int] = mapped_column(
        Integer,
        default=6,
        comment='Количество покупок монеты',
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id', ondelete='CASCADE', name='fk_coin_user_id'),
        nullable=False,
        comment='ID пользователя',
    )
    start: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment='Запущена ли монета на торговлю',
    )
    buy: Mapped[int] = mapped_column(
        Integer,
        default=1,
        comment='Количество закупок',
    )
    user: Mapped["User"] = relationship("User", back_populates="coins")

    def __repr__(self) -> str:
        return f'{self.name}'
