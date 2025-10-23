from typing import Optional

from app.core.config import settings
from app.core.db import AsyncSessionLocal
from app.crud import user_crud
from app.schemas.user import UserCreate


async def add_admin() -> Optional[None]:
    """Создание админа."""
    async with AsyncSessionLocal() as session:
        result = await user_crud.get_user_by_telegram_id(0, session)
        if result is None:
            user_in = UserCreate(
                telegram_id=0,
                password=settings.redis_pass,
            )
            result = await user_crud.create(user_in, session)
            result.is_superuser = True
            await session.commit()
