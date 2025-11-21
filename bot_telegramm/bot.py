from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv
import requests
from pprint import pprint
import aiohttp
from http import HTTPStatus


load_dotenv()
TOKEN_BOT = os.getenv('TOKEN_BOT')
DOMEN = 'http://127.0.0.1:8000'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = f'{DOMEN}/api/v1/user/register'
    data = {"telegram_id": update.message.from_user.id}

    async with aiohttp.ClientSession() as session:
        response = await session.post(url, json=data)

    if response.status == HTTPStatus.CREATED:
        return await update.message.reply_text("Вы успешно зарегистрированы!")
    elif response.status == HTTPStatus.BAD_REQUEST:
        return await update.message.reply_text("Привет! Я работаю 🚀")

    return await update.message.reply_text("Что-то пошло не так.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Список команд:\n/start — старт\n/help — помощь")


def main():
    application = ApplicationBuilder().token(TOKEN_BOT).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.run_polling()


if __name__ == "__main__":
    main()
