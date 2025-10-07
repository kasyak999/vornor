from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.crud.user import user_crud
from app.schemas.user import UserCreate, UserToken, UserDB
from app.api.validators import check_user, check_not_user
from app.models import User
from app.services.user import get_current_user

router = APIRouter(prefix='/user', tags=['Работа с пользователем'])


@router.get(
    "/me",
    response_model=UserDB,
    summary='Личный кабинет',
)
async def get_me(
    token: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Получение информации о пользователе."""
    return await user_crud.get_user_by_telegram_id(token, session)


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
    return await user_crud.create(telegram_id, session)


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
    token = await user_crud.authenticate_user(telegram_id)
    return {"access_token": token, "token_type": "bearer"}
