from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.models import User, Coin
from app.services.user import get_current_user
from app.schemas.coin import CoinCreate, CoinDB, CoinUpdate
from app.crud import coin_crud, user_crud
from app.api.validators import (
    check_coin_user, check_slot_and_coin, check_not_coin_user)
from typing import List

# Создаем главный роутер для API
router = APIRouter(prefix='/coin', tags=['Работа с монетой'])


@router.post(
    "/",
    summary='Добавить монету',
    response_model=CoinDB,
    response_model_exclude_none=True,
)
async def post_coin(
    coin_add: CoinCreate,
    token: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Добавление новой монеты для пользователя."""
    user = await user_crud.get_user_all(token, session)

    # Проверяем есть ли у пользователя слоты для добавления монеты
    await check_slot_and_coin(user.coin_slots, user.coins)

    # Проверяем, что монета с таким именем у пользователя еще не существует
    result_coin = await coin_crud.get_coin_by_name_and_user(
        coin_add.name, user.id, session)
    await check_coin_user(result_coin)

    coin_add.user_id = user.id
    return await coin_crud.create(coin_add, session)


@router.delete(
    '/{coin_id}',
    response_model=CoinDB,
    response_model_exclude_none=True,
    summary='Удаление монеты по ID',
)
async def delete_coin(
        coin_id: int,
        token: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Удаление монеты по ID."""
    user_coins = await coin_crud.all_coins_id_user(token, session)
    coin = next((c for c in user_coins if c.id == coin_id), None)
    await check_not_coin_user(coin)
    return await coin_crud.remove(coin, session)


@router.patch(
    '/{coin_id}',
    response_model=CoinDB,
    response_model_exclude_none=True,
    summary='Изменение монеты',
)
async def patch_coin(
        coin_id: int,
        coin_edit: CoinUpdate,
        token: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Удаление монеты по ID."""
    user_coins = await coin_crud.all_coins_id_user(token, session)
    coin = next((c for c in user_coins if c.id == coin_id), None)
    await check_not_coin_user(coin)

    return await coin_crud.update(coin, coin_edit, session)
