from pydantic import BaseModel, ConfigDict
from typing import Optional


class CoinCreate(BaseModel):
    """Создание монету."""
    name: str
    user_id: Optional[int] = None

    model_config = ConfigDict(extra='forbid')


class CoinDate(BaseModel):
    name: str


class CoinDB(CoinDate):
    """Создание монету."""
    id: int
