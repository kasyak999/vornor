from sqlalchemy import ForeignKey, DateTime
from app.core.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timedelta


def default_end_date():
    """Возвращает текущую дату + 30 дней."""
    dt = datetime.now() + timedelta(days=30)
    return dt.replace(microsecond=0)


class CoinSlot(Base):
    """Модель слота для монеты."""
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        comment='ID пользователя',
    )
    end_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=default_end_date,
        nullable=True,
        comment='Дата окончания слота',
    )

    user: Mapped["User"] = relationship("User", back_populates="coin_slots")

    def __repr__(self) -> str:
        return 'слот'
