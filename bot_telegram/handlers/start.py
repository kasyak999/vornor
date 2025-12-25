from telegram import Update
from telegram.ext import ContextTypes
from http import HTTPStatus
# from loguru import logger
from services.api import ApiService
from keyboards.main_keyboard import get_main_keyboard


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    keyboard = None
    message = "Что-то пошло не так."

    response = await ApiService.register_user(telegram_id)

    if response.status == HTTPStatus.OK:
        message = "Вы успешно зарегистрированы!\nНажмите /start"

    elif response.status == HTTPStatus.CONFLICT:
        token_response = await ApiService.get_token(telegram_id)

        if token_response.status == HTTPStatus.OK:
            data = await token_response.json()
            context.user_data["token"] = data.get("access_token")
            message = "Добро пожаловать 🚀"
            keyboard = get_main_keyboard()

    return await update.message.reply_text(
        message,
        reply_markup=keyboard)
