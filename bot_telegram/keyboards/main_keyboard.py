from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("Личный кабинет", callback_data="lk")],
        [InlineKeyboardButton("Помощь", callback_data="help")],
    ]
    return InlineKeyboardMarkup(keyboard)
