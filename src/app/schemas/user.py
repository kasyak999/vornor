from pydantic import BaseModel


class UserCreate(BaseModel):
    """Создание пользователя."""
    telegram_id: int


class UserToken(BaseModel):
    """Получение токена."""
    access_token: str
    token_type: str


class UserDB(BaseModel):
    id: int
    telegram_id: int
