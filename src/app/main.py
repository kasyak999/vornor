from fastapi import FastAPI
from app.core.config import settings
from app.api.routers import api_router

from sqladmin import Admin
from app.core.admin import (
    AdminAuth, UserAdmin, CoinAdmin, CoinSlotAdmin)
from app.core.db import engine

app = FastAPI(
    title=settings.app_title,
    description=settings.description,
)

app.include_router(api_router)

authentication_backend = AdminAuth(secret_key=settings.secret)
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(CoinAdmin)
admin.add_view(CoinSlotAdmin)
