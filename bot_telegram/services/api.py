import aiohttp
from http import HTTPStatus
from config import DOMEN


class ApiService:

    @staticmethod
    async def register_user(telegram_id: int):
        """ Регистрация пользователя в боте. """
        url = f"{DOMEN}/api/v1/user/register"
        async with aiohttp.ClientSession() as session:
            return await session.post(url, json={"telegram_id": telegram_id})

    @staticmethod
    async def get_token(telegram_id: int):
        """ Получение токена пользователя. """
        url = f"{DOMEN}/api/v1/user/token"
        async with aiohttp.ClientSession() as session:
            return await session.post(url, params={"telegram_id": telegram_id})

    @staticmethod
    async def get_user(headers: dict):
        """ Получение данных пользователя. """
        url = f"{DOMEN}/api/v1/user/"
        async with aiohttp.ClientSession() as session:
            return await session.get(url, headers=headers)
