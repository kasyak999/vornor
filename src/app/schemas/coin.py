from pydantic import BaseModel, ConfigDict
from typing import Optional


class CoinCreate(BaseModel):
    """Создание монету."""
    name: str
    user_id: Optional[int] = None

    model_config = ConfigDict(extra='forbid')


class CoinUpdate(BaseModel):
    """Создание монету."""
    name: Optional[str] = None
    buy_usdt: Optional[float] = None
    cycle: Optional[bool] = False
    price_buy: Optional[float] = None
    count_buy: Optional[int] = None

    model_config = ConfigDict(extra='forbid')


class CoinDB(CoinUpdate):
    """Информация о монете."""
    id: int
