from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session


# Создаем главный роутер для API
router = APIRouter(prefix='/coin', tags=['Работа с монетой'])


@router.get(
    '/test',
    summary='Тестовый эндпоинт',
)
async def test(
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Тест."""
    return {'status': 'тест'}
