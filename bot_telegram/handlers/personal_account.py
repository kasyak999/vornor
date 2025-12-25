from telegram import Update
from telegram.ext import ContextTypes
from http import HTTPStatus
# from loguru import logger
from services.api import ApiService

# НЕ ГОТОВО

async def personal_account(update: Update, context: ContextTypes.DEFAULT_TYPE):

    token = context.user_data.get("token")
    if not token:
        return await update.message.reply_text("Сессия истекла. /start")

    headers = {"Authorization": f"Bearer {token}"}
    response = await ApiService.get_user(headers)

    if response.status == HTTPStatus.OK:
        data = await response.json()
        text = (
            "Ваш личный кабинет:\n\n"
            f"Слоты для монет: {data.get('count_clots')}\n"
            f"Что-то ещё: {data.get('qwe')}"
        )
        return await update.callback_query.edit_message_text(
            text, reply_markup=get_main_keyboard()
        )

    return await update.callback_query.edit_message_text(
        "Что-то пошло не так."
    )


async def personal_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Команда /lk - личный кабинет пользователя. """
    url = f'{DOMEN}/api/v1/user/'
    token = context.user_data.get("token") if context.user_data else None
    headers = {"Authorization": f"Bearer {token}"}

    async with aiohttp.ClientSession() as session:
        response = await session.get(url, headers=headers)

    if response.status in (
            HTTPStatus.UNAUTHORIZED, HTTPStatus.BAD_REQUEST):
        return await update.message.reply_text(
            "Ссессия истекла, пожалуйста, выполните /start"
        )

    if response.status == HTTPStatus.OK:
        response_json = await response.json()
        # return await update.message.reply_text(
        #     f"Ваш личный кабинет: {response_json}"
        # )
        pprint(response_json)
        text = (
            'Ваш личный кабинет:\n\n'
            f'Слоты для монет: {response_json.get("count_clots")}\n'
            f'Слоты для монет: {response_json.get("qwe")}'
        )
        return await update.callback_query.edit_message_text(
            text,
            reply_markup=get_main_keyboard()
        )
    pprint(response.status)
    await update.message.reply_text("Что-то пошло не так.")