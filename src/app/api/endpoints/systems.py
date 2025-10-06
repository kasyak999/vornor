from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session


# Создаем главный роутер для API
router = APIRouter(prefix='/systems', tags=['Системные'])


@router.get(
    '/ping_db',
    summary='Проверка подключения к базе данных',
    description=(
        'Этот эндпоинт выполняет простой SQL-запрос `SELECT 1`, '
        'чтобы убедиться, что соединение с базой данных установлено.'
    ),
    response_description='Статус соединения и результат запроса',
)
async def ping_db(
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Проверка подключения к базе данных."""
    try:
        result = await session.execute(text('SELECT 1'))
        return {'status': 'ok', 'result': result.scalar()}
    except SQLAlchemyError as e:
        return {'status': 'ошибка', 'detail': str(e)}
