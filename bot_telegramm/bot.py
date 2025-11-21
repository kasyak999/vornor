from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv
from pprint import pprint
import aiohttp
from http import HTTPStatus


load_dotenv()
TOKEN_BOT = os.getenv('TOKEN_BOT')
DOMEN = 'http://127.0.0.1:8000'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Команда /start - регистрация пользователя в боте. """
    url = f'{DOMEN}/api/v1/user/register'
    data = {"telegram_id": update.message.from_user.id}

    async with aiohttp.ClientSession() as session:
        response = await session.post(url, json=data)

    if response.status == HTTPStatus.OK:
        return await update.message.reply_text(
            "Вы успешно зарегистрированы!\nНажмите /start")
    elif response.status == HTTPStatus.CONFLICT:
        url = f'{DOMEN}/api/v1/user/token'
        async with aiohttp.ClientSession() as session:
            response_token = await session.post(url, params=data)

        if response_token.status == HTTPStatus.OK:
            response_token_json = await response_token.json()
            context.user_data["token"] = response_token_json.get(
                "access_token")
            return await update.message.reply_text(
                "Привет! Я работаю 🚀\n Посомтреть личный кабинет /lk")

    print(response.status)
    await update.message.reply_text("Что-то пошло не так.")


async def personal_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Команда /lk - личный кабинет пользователя. """
    url = f'{DOMEN}/api/v1/user/'
    token = context.user_data.get("token") if context.user_data else None
    headers = {"Authorization": f"Bearer {token}"}

    async with aiohttp.ClientSession() as session:
        response = await session.get(url, headers=headers)

    if response.status == HTTPStatus.OK:
        response_json = await response.json()
        return await update.message.reply_text(
            f"Ваш личный кабинет: {response_json}"
        )
    if response.status in (
            HTTPStatus.UNAUTHORIZED, HTTPStatus.BAD_REQUEST):
        return await update.message.reply_text(
            "Ссессия истекла, пожалуйста, выполните /start"
        )

    pprint(response.status)
    await update.message.reply_text("Что-то пошло не так.")


def main():
    application = ApplicationBuilder().token(TOKEN_BOT).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("lk", personal_account))
    application.run_polling()


if __name__ == "__main__":
    main()
