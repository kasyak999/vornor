from fastapi import HTTPException
from http import HTTPStatus
from app.models import User


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
