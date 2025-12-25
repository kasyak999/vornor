from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler)
from loguru import logger
from config import TOKEN_BOT
from handlers import start


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главный callback-router."""
    query = update.callback_query
    await query.answer()

    if query.data == "lk":
        return await personal_account(update, context)

    # if query.data == "help":
    #     return await help_handler(update, context)


def main():
    logger.info("Запуск Telegram-бота")

    application = ApplicationBuilder().token(TOKEN_BOT).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(menu_callback))
    application.run_polling()


if __name__ == "__main__":
    main()
