from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    """Создание пользователя."""
    telegram_id: int
    password: Optional[str] = None


class UserToken(BaseModel):
    """Получение токена."""
    access_token: str
    token_type: str


class UserDB(BaseModel):
    id: int
    telegram_id: int
