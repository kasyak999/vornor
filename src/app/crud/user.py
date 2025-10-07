from app.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base_crud import CRUDBase
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 день


class UserCrud(CRUDBase):
    """CRUD операции для модели User."""

    async def get_user_by_telegram_id(
        self,
        telegram_id: int,
        session: AsyncSession
    ):
        """Получение пользователя по telegram_id."""
        result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
        return result.scalar_one_or_none()

    async def authenticate_user(
        self,
        telegram_id: int,
    ):
        """Получить токен."""
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {'sub': str(telegram_id), 'exp': expire}
        return jwt.encode(to_encode, settings.secret, algorithm=ALGORITHM)


user_crud = UserCrud(User)
