from sqlalchemy import Column, Integer, DateTime
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from datetime import datetime
from sqlalchemy.orm import (
    declarative_base, declared_attr, mapped_column, Mapped
)
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.sql import func
from app.core.config import settings


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )


Base = declarative_base(cls=PreBase)
engine = create_async_engine(settings.database_url)
# AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
