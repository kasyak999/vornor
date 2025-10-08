from typing import Generic, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый класс для CRUD операций с моделями."""

    def __init__(self, model: Type[ModelType]) -> None:
        """Инициализация CRUD класса с указанием модели."""
        self.model = model

    async def create(
        self,
        obj_in,
        session: AsyncSession,
    ):
        """Создать новый объект."""
        obj_in_data = obj_in.model_dump()

        if obj_in_data["password"] is not None:
            obj_in_data["password"] = pwd_context.hash(obj_in_data["password"])

        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj: ModelType,
        session: AsyncSession,
    ) -> ModelType:
        """Удалить объект."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj
