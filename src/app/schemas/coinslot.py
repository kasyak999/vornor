from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CoinSlotCreate(BaseModel):
    """Создание пользователя."""
    user_id: int
    end_date: Optional[datetime] = None


class CoinSlotData(BaseModel):
    end_date: Optional[datetime] = None


class CoinSlotDB(CoinSlotData):
    user_id: int
