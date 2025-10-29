from pybit.unified_trading import HTTP
from fastapi import HTTPException
from http import HTTPStatus
from pprint import pprint
from starlette.concurrency import run_in_threadpool
from pybit.exceptions import InvalidRequestError
from app.models import User
from decimal import Decimal, ROUND_DOWN


async def bybit_session(api_key: str, api_secret: str, demo=False) -> HTTP:
    """Создание сессии Bybit."""
    return HTTP(
        api_key=api_key,
        api_secret=api_secret,
        demo=demo,
    )


async def validate_bybit_keys(api_key: str, api_secret: str) -> bool:
    """Проверка валидности API ключей Bybit."""

    networks = [
        ("real", False),
        ("demo", True),
    ]
    for network_name, demo_mode in networks:
        try:
            session = await bybit_session(api_key, api_secret, demo_mode)
            result = await run_in_threadpool(session.get_api_key_information)
            if result.get("retCode") == 0:
                return demo_mode
        except InvalidRequestError as e:
            if 'ErrCode: 10003' in str(e):
                continue
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Ошибка проверки ключей ({network_name}): {e}"
            ) from e
    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail="Неизместная ошибка попробуйте позже."
    )


async def bybit_balance(user: User) -> dict:
    """Получить баланс монет с bybit"""

    session = await bybit_session(
        user.api_key,
        user.api_secret,
        user.demo
    )

    try:
        response = await run_in_threadpool(
            session.get_wallet_balance,
            accountType="UNIFIED"
        )
        coins = response.get("result", {}).get("list", [{}])[0].get("coin", [])
    except InvalidRequestError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Ошибка при запросе к Bybit: {e}"
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Неожиданный формат ответа от Bybit."
        ) from e

    if not response:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="В портфеле пока нет монет."
        )

    return {
        value["coin"]: {
            "balance": value["walletBalance"],
            "usd_value": value["usdValue"],
        }
        for value in coins
    }


async def get_info_coin(user: User, symbol: str):
    """Получить информацию по монетам с Bybit"""
    symbol = symbol + "USDT"
    session = await bybit_session(user.api_key, user.api_secret, user.demo)
    try:
        result = await run_in_threadpool(
            session.get_instruments_info, category="spot", symbol=symbol)
        result = result.get("result", {}).get("list", [])
        if not result:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Монета {symbol} не найдена"
            )

        znak_price = result[0]["priceFilter"]['tickSize']
        znak_price = abs(Decimal(str(znak_price)).as_tuple().exponent)
        result[0]['znak_price'] = znak_price

        base_precision = result[0]["lotSizeFilter"]["basePrecision"]
        base_precision = abs(Decimal(str(base_precision)).as_tuple().exponent)
        result[0]['base_precision'] = base_precision

        return result[0]
    except InvalidRequestError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Ошибка запроса к Bybit: {e}"
        ) from e


async def bybit_coin_balance(user: User, coin: str) -> dict:
    """Получить баланс определеной монеты с bybit"""

    session = await bybit_session(
        user.api_key,
        user.api_secret,
        user.demo
    )

    try:
        response = await run_in_threadpool(
            session.get_wallet_balance,
            accountType="UNIFIED"
        )
        coins = response.get("result", {}).get("list", [{}])[0].get("coin", [])
    except InvalidRequestError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Ошибка при запросе к Bybit: {e}"
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Неожиданный формат ответа от Bybit."
        ) from e

    if not response:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="В портфеле пока нет монет."
        )

    for value in coins:
        if value["coin"] == coin:
            return {
                "balance": value["walletBalance"],
                "usd_value": value["usdValue"],
            }

    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail=f"Монеты {coin} нет в портфеле."
    )


async def add_coin_order(
    user: User,
    symbol: str,
    qty,
    price,
    side: str,
):
    """ Создать лимитный ордер """

    session = await bybit_session(
        user.api_key,
        user.api_secret,
        user.demo
    )

    try:
        await run_in_threadpool(
            session.place_order,
            category="spot",  # спотовый рынок
            symbol=symbol,  # торговая пара
            side=side,  # "Buy" или "Sell"
            orderType="Limit",  # лимитный ордер
            qty=qty,  # количество базовой валюты
            price=price,  # цена лимитного ордера
        )
    except InvalidRequestError as e:
        return (
            f'{symbol}: {side} Ошибка API при создании ордера: {str(e)}')
    else:
        return f'✅ {symbol}: {side} ордер создан'


def round_down(balance: Decimal, base_precision: int) -> Decimal:
    """
    Округляет вниз до заданного количества знаков после запятой.
    """
    quantize_value = Decimal(f"1e-{base_precision}")
    return balance.quantize(quantize_value, rounding=ROUND_DOWN)


async def list_orders(user: User, symbol: str):
    """ Список ордеров """
    symbol = symbol + "USDT"
    session = await bybit_session(
        user.api_key,
        user.api_secret,
        user.demo
    )

    orders = await run_in_threadpool(
        session.get_open_orders, category="spot", symbol=symbol)
    orders = orders.get("result", {}).get("list", [])
    result = []
    for coin in orders:
        result.append({
            coin['side']: int(coin['orderId']),
        })
    return result
