from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.crud import user_crud, coinslot_crud
from app.schemas.user import (
    UserCreate, UserToken, UserDB, UserUpdate, UserAllDB)
from app.api.validators import check_user, check_not_user
from app.models import User
from app.services.user import get_current_user
from app.schemas.coinslot import CoinSlotCreate
from app.services.bybit import validate_bybit_keys
import app.tasks as tasks


router = APIRouter(prefix='/user', tags=['Работа с пользователем'])


@router.post(
    "/register",
    summary='Регистрация',
    response_model=UserDB,
)
async def register(
    telegram_id: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Регистрация нового пользователя."""
    user = await user_crud.get_user_by_telegram_id(
        telegram_id.telegram_id, session)
    await check_user(user)
    result = await user_crud.create(telegram_id, session)
    await coinslot_crud.create(CoinSlotCreate(user_id=result.id), session)
    return result


@router.post(
    "/token",
    summary='Получение токена',
    response_model=UserToken,
)
async def post_token(
    telegram_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Токен для зарегистрированного пользователя."""
    user = await user_crud.get_user_by_telegram_id(
        telegram_id, session)
    await check_not_user(user)
    token = await user_crud.authenticate_user(user.id)
    return {"access_token": token, "token_type": "bearer"}


@router.get(
    "/",
    response_model=UserAllDB,
    summary='Личный кабинет',
    response_model_exclude_none=True
)
async def get_me(
    token: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Получение информации о пользователе."""
    return await user_crud.get_user_all(token, session)


@router.patch(
    "/",
    response_model=UserDB,
    summary='Обновление данных пользователя',
)
async def patch_me(
    obj_in: UserUpdate,
    token: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Обновление данных пользователя."""
    user = await user_crud.get_user_all(token, session)
    obj_in.demo = await validate_bybit_keys(obj_in.api_key, obj_in.api_secret)
    user.coins.clear()
    return await user_crud.update(user, obj_in, session)


@router.get("/ping_celery", summary="Проверка Celery")
async def ping_celery() -> dict:
    """Проверка работы Celery."""
    try:
        tasks.test_task.apply_async()  # Отправляем задачу в очередь
        tasks.test_task2.apply_async(countdown=5)  # запуск через 5 секунд
        return {"message": "Если нет ошибки все ок"}
    except Exception as e:
        return {"error": str(e)}
