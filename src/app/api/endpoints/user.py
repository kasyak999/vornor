from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from app.core.db import get_async_session
from app.crud import user_crud, coinslot_crud
from app.schemas.user import UserCreate, UserToken, UserDB, UserUpdate, UserAllDB
from app.api.validators import check_user, check_not_user
from app.models import User
from app.services.user import get_current_user
from app.schemas.coinslot import CoinSlotCreate


router = APIRouter(prefix='/user', tags=['Работа с пользователем'])


@router.get(
    "/me",
    response_model=UserAllDB,
    summary='Личный кабинет',
)
async def get_me(
    token: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Получение информации о пользователе."""
    return await user_crud.get_user_all(token, session)


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
    print(user.id)
    await check_not_user(user)
    token = await user_crud.authenticate_user(user.id)
    return {"access_token": token, "token_type": "bearer"}


@router.patch(
    "/me",
    response_model=UserDB,
    summary='Обновление данных пользователя',
)
async def patch_me(
    obj_in: UserUpdate,
    token: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Получение информации о пользователе."""
    user = await user_crud.get_id(token, session)
    return await user_crud.update(user, obj_in, session)
