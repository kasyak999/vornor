from pybit.unified_trading import HTTP
from fastapi import HTTPException
from http import HTTPStatus
from pprint import pprint
from starlette.concurrency import run_in_threadpool
from pybit.exceptions import InvalidRequestError


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
            session = await bybit_session(api_key, api_secret, demo=demo_mode)
            result = await run_in_threadpool(session.get_api_key_information)
            if result.get("retCode") == 0:
                return demo_mode
        except InvalidRequestError as e:
            if "10003" in str(e):
                continue
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Ошибка проверки ключей ({network_name}): {e}"
            ) from e
        except Exception as e:
            # Обработка Retryable error
            if "Retryable error occurred" in str(e):
                raise HTTPException(
                    status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                    detail=f"Bybit временно недоступен ({network_name}): попробуйте позже"
                ) from e
            raise  # другие ошибки пусть поднимаются как есть

    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail="Неверные ключи Bybit: не подходят ни для real, ни для demo"
    )


async def bybit_balance(user) -> dict:
    """Получить баланс монет с bybit"""

    session = await bybit_session(
        user.api_key,
        user.api_secret,
        demo=user.demo
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
