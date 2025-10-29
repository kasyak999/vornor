from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.crud import user_crud
from app.models import User
from app.services.user import get_current_user
from app.services.bybit import (
    bybit_balance, bybit_coin_balance, get_info_coin, list_orders)


router = APIRouter(prefix='/bybit', tags=['Работа с bybit'])


@router.get(
    "/",
    summary='Получить весь портфель',
    response_model=dict,
    responses={
        200: {
            "description": "Успешный ответ",
            "content": {
                "application/json": {
                    "example": {
                        "BTC": {"balance": "0.0023", "usd_value": "125.60"},
                        "ETH": {"balance": "0.104", "usd_value": "182.42"},
                    }
                }
            },
        },
        400: {
            "description": "Ошибка запроса",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {"Ошибка при запросе к Bybit"},
                    },
                }
            },
        },
    },
)
async def get_bybit(
    token: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """"Возвращает баланс монет с Bybit."""
    user = await user_crud.get_id(token, session)
    return await bybit_balance(user)


@router.get(
    "/{coin_name}",
    summary='Получить баланс определенной монеты',
    response_model=dict,
    responses={
        200: {
            "description": "Успешный ответ",
            "content": {
                "application/json": {
                    "example": {"balance": "0.0023", "usd_value": "125.60"}
                }
            },
        },
        400: {
            "description": "Ошибка запроса",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {"Ошибка при запросе к Bybit"},
                    },
                }
            },
        },
    },
)
async def get_coins_balamce(
    coin_name: str,
    token: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """"Возвращает баланс монеты с Bybit."""
    user = await user_crud.get_id(token, session)
    coin_name = coin_name.upper()
    return await bybit_coin_balance(user, coin_name)


@router.get(
    "/info/{coin_name}",
    summary='Получить информацию по монете',
    response_model=dict,
    responses={
        200: {
            "description": "Успешный ответ",
            "content": {
                "application/json": {
                    "example": {
                        "symbol": "BTCUSDT",
                        "bid_price": "45000.00",
                        "ask_price": "45100.00",
                        "last_price": "45050.00",
                    }
                }
            },
        },
        400: {
            "description": "Ошибка запроса",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {"Ошибка при запросе к Bybit"},
                    },
                }
            },
        },
    },
)
async def get_coin_info(
    coin_name: str,
    token: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """"Возвращает информацию по монете с Bybit."""
    user = await user_crud.get_id(token, session)
    coin_name = coin_name.upper()
    return await get_info_coin(user, coin_name)


@router.get(
    "/order/{coin_name}",
    summary='Получить открытые ордера по монете',
    response_model=list,
)
async def get_coin_order(
    coin_name: str,
    token: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """"Получить открытые ордера по монете на Bybit."""
    user = await user_crud.get_id(token, session)
    coin_name = coin_name.upper()
    return await list_orders(user, coin_name)
