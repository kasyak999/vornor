from fastapi import FastAPI, Request
from app.core.config import settings
from app.api.routers import api_router

from sqladmin import Admin
from app.core.admin import (
    AdminAuth, UserAdmin, CoinAdmin, CoinSlotAdmin)
from app.core.db import engine
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from loguru import logger
import sys
from app.core.init_db import add_admin
from fastapi.middleware.trustedhost import TrustedHostMiddleware


logger.remove()
logger.add(
    sys.stdout,
    format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}',
    level='INFO',
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Контекстный менеджер для инициализации приложения."""
    logger.info('Запуск приложения')
    await add_admin()
    yield
    logger.info('Завершение работы приложения')

app = FastAPI(
    title=settings.app_title,
    description=settings.description,
    lifespan=lifespan,
)

app.include_router(api_router)

# Доверяем прокси, которые передают заголовки
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])


authentication_backend = AdminAuth(secret_key=settings.secret)
admin = Admin(
    app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(CoinAdmin)
admin.add_view(CoinSlotAdmin)


@app.get("/check")
def check(request: Request):
    return {
        "scheme": request.url.scheme,
        "host": request.url.hostname,
        "port": request.url.port
    }