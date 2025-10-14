from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List
from passlib.context import CryptContext
from .coinslot import CoinSlotData
from .coin import CoinDB


class UserCreate(BaseModel):
    """Создание пользователя."""
    telegram_id: int
    password: Optional[str] = None

    model_config = ConfigDict(extra='forbid')

    @field_validator('password')
    @classmethod
    def validate_password(cls, password_value: str) -> str:
        """Валидация пароля."""
        pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
        return pwd_context.hash(password_value)


class UserToken(BaseModel):
    """Получение токена."""
    access_token: str
    token_type: str


class UserDB(BaseModel):
    id: int
    telegram_id: int
    api_key: Optional[str] = None


class UserAllDB(UserDB):
    coin_slots: List[CoinSlotData] = []
    coins: List[CoinDB] = []


class UserUpdate(BaseModel):
    """Обновление пользователя."""
    api_key: Optional[str] = None

    model_config = ConfigDict(extra='forbid')
