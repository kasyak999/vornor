from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional


class CoinBase(BaseModel):
    """Базовый класс"""
    buy_usdt: Optional[float] = None
    cycle: Optional[bool] = False
    price_buy: Optional[float] = None
    count_buy: Optional[int] = None
    start: Optional[bool] = False


class CoinCreate(BaseModel):
    """Создание монету."""
    name: str
    user_id: Optional[int] = None

    model_config = ConfigDict(extra='forbid')


class CoinUpdate(CoinBase):
    """Изменить монету."""
    model_config = ConfigDict(extra='forbid')

    @field_validator('price_buy')
    @classmethod
    def validate_price_buy(cls, price_buy: float) -> float:
        """Проверка цены покупки."""
        if price_buy <= 0:
            raise ValueError("price_buy должен быть больше нуля.")
        return price_buy

    @field_validator('count_buy')
    @classmethod
    def validate_count_buy(cls, count_buy: int) -> int:
        """Проверка количества покупок."""
        if count_buy <= 0:
            raise ValueError("count_buy должен быть больше нуля.")
        return count_buy

    @field_validator('buy_usdt')
    @classmethod
    def validate_buy_usdt(cls, count_buy: float) -> float:
        """Проверка цены перой закупки."""
        if count_buy < 5.5:
            raise ValueError(
                "buy_usdt должен быть больше 5.5 usdt или равен 5.5.")
        return count_buy


class CoinDB(CoinBase):
    """Информация о монете."""
    id: int
    name: str
    buy: int
