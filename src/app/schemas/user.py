from pydantic import (
    BaseModel, ConfigDict, field_validator, model_validator, computed_field)
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
    api_secret: Optional[str] = None
    demo: Optional[bool] = None


class UserAllDB(UserDB):
    coin_slots: List[CoinSlotData] = []
    coins: List[CoinDB] = []

    @computed_field
    def count_clots(self) -> int:
        """Возвращает количество слотов."""
        return len(self.coin_slots)


class UserUpdate(BaseModel):
    """Обновление пользователя."""
    api_key: str
    api_secret: str
    demo: Optional[bool] = None

    model_config = ConfigDict(extra='forbid')

    # @model_validator(mode='after')
    # def validate_keys_together(self) -> "UserUpdate":
    #     """Синхронная валидация (асинхронное вынести наружу)."""
    #     if self.api_key and not self.api_secret:
    #         raise ValueError("api_secret и api_key должны быть указаны.")
    #     return self
