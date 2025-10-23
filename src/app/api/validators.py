from fastapi import HTTPException
from http import HTTPStatus
from app.models import User, Coin
from app.schemas.coin import CoinUpdate


async def check_user(user: User | None) -> None:
    """Проверка пользователя на существование"""
    if user is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Пользователь уже зарегистрирован")


async def check_not_user(user: User | None) -> None:
    """Проверка пользователя на существование"""
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Пользователь не зарегистрирован")


async def check_coin_user(result: Coin | None) -> None:
    """Проверка на дубли монет у пользователя"""
    if result is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Такая монета уже есть")


async def check_not_coin_user(result: Coin | None, user_id: int) -> None:
    """Проверка монеты на существование у пользователя"""
    if result is None or result.user_id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Такой монеты нет")


async def check_slot_and_coin(user: User) -> None:
    """Проверка слотов и монет у пользователя"""
    if user.demo:
        return
    if len(user.coins) >= len(user.coin_slots):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Недостаточно слотов для добавления монеты")


async def check_has_api_key(user: User) -> None:
    """Проверка наличия API ключа у пользователя"""
    if not user.api_key or not user.api_secret:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Не установлен API ключ или API секрет")


async def validate_start_coin(coin: Coin, coin_update: CoinUpdate) -> None:
    """Валидация при старте монеты"""
    price = coin_update.price_buy or coin.price_buy
    if coin_update.start and price is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Для запуска монеты необходимо указать price_buy.")
