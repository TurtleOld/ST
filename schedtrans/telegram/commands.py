from typing import Any

from schedtrans.telegram.config import bot


@bot.message_handler(commands=['start'])
async def start_command_bot(message):
    await bot.send_message(message.chat.id, 'Бот запущен!')


def start_bot() -> Any:
    """Function for start telegram bot"""
    return bot.infinity_polling()
