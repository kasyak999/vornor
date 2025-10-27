from pybit.unified_trading import HTTP
from fastapi import HTTPException
from http import HTTPStatus
from pprint import pprint
from starlette.concurrency import run_in_threadpool
from pybit.exceptions import InvalidRequestError
from app.models import User


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
            session.get_tickers, category="spot", symbol=symbol)
        tickers = result.get("result", {}).get("list", [])
        if not tickers:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Монета {symbol} не найдена"
            )
        return tickers[0]
    except InvalidRequestError as e:
        if "10001" in str(e):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Такой монеты нет: {symbol}"
            ) from e
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
