from fastapi import APIRouter
from app.api.endpoints import systems_router, coin_router


# Создаем главный роутер для API
api_router = APIRouter(prefix='/api/v1')
api_router.include_router(systems_router)
api_router.include_router(coin_router)
