from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import inspect
from passlib.context import CryptContext

from app.core.db import engine
from app.models import User, Coin, CoinSlot


def get_column_comments(model):
    mapper = inspect(model)
    labels = {}
    for column in mapper.columns:
        if column.comment:
            labels[column.name] = column.comment
    return labels


class UserAdmin(ModelView, model=User):
    column_list = [
        User.telegram_id, User.coins, User.coin_slots,
        User.demo, User.created_at]
    name = "пользователя"
    name_plural = "Пользователи"
    column_labels = {**get_column_comments(User), **{
        "coins": "Монеты",
        "coin_slots": "Слоты монет",
    }}


class CoinAdmin(ModelView, model=Coin):
    column_list = [
        Coin.name, Coin.user_id, Coin.cycle, Coin.start, Coin.created_at]
    name = "монету"
    name_plural = "Монеты"
    column_labels = get_column_comments(Coin)


class CoinSlotAdmin(ModelView, model=CoinSlot):
    column_list = [
        "user.telegram_id", CoinSlot.end_date, CoinSlot.created_at]
    name = "слот монеты"
    name_plural = "Слоты монет"
    column_labels = get_column_comments(CoinSlot)


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        telegram_id = form.get('username')
        hashed_password = form.get('password')

        try:
            telegram_id = int(telegram_id)
        except (TypeError, ValueError):
            return False

        async with AsyncSession(engine) as session:
            result = await session.execute(select(User).where(
                User.telegram_id == telegram_id))
            user = result.scalar_one_or_none()
        if not user:
            return False
        if not pwd_context.verify(hashed_password, user.password):
            return False
        if not user.is_superuser:
            return False

        request.session.update({"user": user.telegram_id})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return "user" in request.session
