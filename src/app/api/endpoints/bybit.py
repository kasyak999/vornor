from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.crud import user_crud
from app.models import User
from app.services.user import get_current_user
from app.services.bybit import bybit_balance


router = APIRouter(prefix='/bybit', tags=['Работа с bybit'])


@router.get(
    "/",
    summary='Получить портфель пользователя на Bybit',
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
