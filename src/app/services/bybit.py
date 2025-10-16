from pybit.unified_trading import HTTP
from fastapi import HTTPException
from http import HTTPStatus
from pprint import pprint
from starlette.concurrency import run_in_threadpool
from pybit.exceptions import InvalidRequestError


def bybit_session(api_key: str, api_secret: str, demo=False) -> HTTP:
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
            session = bybit_session(api_key, api_secret, demo=demo_mode)
            result = await run_in_threadpool(session.get_api_key_information)
            if result.get("retCode") == 0:
                return demo_mode
        except InvalidRequestError as e:
            if "10003" not in str(e):
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f"Ошибка проверки ключей {network_name}: {e}"
                ) from e

    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail="Неверные ключи Bybit: не подходят ни для real, ни для demo"
    )
