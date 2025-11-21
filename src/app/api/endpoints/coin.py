from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.models import User
from app.services.user import get_current_user
from app.schemas.coin import CoinCreate, CoinDB, CoinUpdate
from app.crud import coin_crud, user_crud
from app.api.validators import (
    check_coin_user, check_slot_and_coin, check_not_coin_user,
    check_has_api_key, validate_start_coin)
from app.services.bybit import get_info_coin, delete_coin_order


# Создаем главный роутер для API
router = APIRouter(prefix='/coin', tags=['Работа с монетой'])


@router.post(
    "/",
    summary='Добавить новую монету.',
    response_model=CoinDB,
    response_model_exclude_none=True,
)
async def post_coin(
    coin_add: CoinCreate,
    token: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    **name** название монеты\n
    **user_id** указывается автоматически
    """
    user = await user_crud.get_user_all(token, session)
    # Проверяем есть ли api ключ у пользователя
    await check_has_api_key(user)
    # Проверяем есть ли у пользователя слоты для добавления монеты
    await check_slot_and_coin(user)
    coin_add.name = coin_add.name.upper()
    # Проверяем, что монета с таким именем у пользователя еще не существует
    result_coin = await coin_crud.get_coin_user(
        coin_add.name, user.id, session)
    await check_coin_user(result_coin)
    coin_add.user_id = user.id
    # Проверка монеты на Bybit
    await get_info_coin(user, coin_add.name)
    return await coin_crud.create(coin_add, session)


@router.delete(
    '/{coin_id}',
    response_model=CoinDB,
    response_model_exclude_none=True,
    summary='Удалить монету.',
)
async def delete_coin(
        coin_id: int,
        token: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session),
):
    """
    **coin_id** id монеты
    """
    user_coins = await coin_crud.get_coin_all(coin_id, session)
    await check_not_coin_user(user_coins, token)

    # Удаляем ордера с биржи
    await delete_coin_order(user_coins.user, user_coins.name)

    return await coin_crud.remove(user_coins, session)


@router.patch(
    '/{coin_id}',
    response_model=CoinDB,
    response_model_exclude_none=True,
    summary='Изменить монету.',
)
async def patch_coin(
        coin_id: int,
        coin_edit: CoinUpdate,
        token: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session),
):
    """
    **coin_id** id монеты\n
    **buy_usdt** На сколько USDT покупать монету если стоит в цикле\n
    **cycle** Зацикливание монеты true / false на покупку и продажу\n
    **price_buy** Курс покупки монеты\n
    **count_buy** Количество покупок монеты, при просадке курса\n
    **start** Запуск монеты в торговлю\n
    """
    user_coins = await coin_crud.get_id(coin_id, session)
    await check_not_coin_user(user_coins, token)
    await validate_start_coin(user_coins, coin_edit)
    return await coin_crud.update(user_coins, coin_edit, session)
