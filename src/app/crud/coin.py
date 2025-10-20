from app.models import Coin
from app.crud.base_crud import CRUDBase
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CoinCrud(CRUDBase):
    """CRUD операции для модели Coin."""

    # async def all_coins_user(
    #     self,
    #     user_id: int,
    #     session: AsyncSession
    # ):
    #     """Получение всех монет по ID пользователя."""
    #     result = await session.execute(
    #             select(Coin).where(Coin.user_id == user_id)
    #         )
    #     return result.scalars().all()

    async def get_coin_user(
        self,
        name: str,
        user_id: int,
        session: AsyncSession
    ):
        """Получение монеты по имени и ID пользователя."""
        stmt = select(Coin).where(Coin.name == name, Coin.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


coin_crud = CoinCrud(Coin)
