from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CoinSlotCreate(BaseModel):
    """Создание пользователя."""
    user_id: int
    end_date: Optional[datetime] = None
