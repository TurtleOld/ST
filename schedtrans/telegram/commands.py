import json
import os
from typing import Any

from telebot import types

from schedtrans.telegram.common import SentMessage, prepare_json_file_route
from schedtrans.telegram.config import bot
from schedtrans.telegram.keyboards import select_transport_type, selected_transport_type


@bot.message_handler(commands=['start'])
async def start_command_bot(message):
    await bot.send_message(message.chat.id, 'Бот запущен!')


@bot.message_handler(commands=['select'])  # type: ignore
async def handler_command_request(message: types.Message) -> None:
    await select_transport_type(message)


class CallBackQueryHandlerTransportType:
    @staticmethod
    @bot.callback_query_handler(func=lambda call: call.data in ['bus', 'suburban'])
    async def callback_handle_transport_type(call: types.CallbackQuery) -> None:
        await bot.delete_message(call.message.chat.id, call.message.id)
        if call.data == 'bus':
            sent_message = await bot.send_message(
                call.message.chat.id,
                'Выбран вид транспорта: Автобус',
            )
            SentMessage.send_message.append(sent_message)
            await selected_transport_type(call.message, call.data)
        elif call.data == 'suburban':
            sent_message = await bot.send_message(
                call.message.chat.id,
                'Выбран вид транспорта: Электричка',
            )
            SentMessage.send_message.append(sent_message)
            await selected_transport_type(call.message, call.data)
    
    @staticmethod
    def prepare_callback_key():
        json_route = prepare_json_file_route()
        for key in json_route:
            return [key]
    
    @staticmethod
    @bot.callback_query_handler(func=lambda call: call.data in [key for key in prepare_json_file_route])
    async def callback_handle_transport_type(call: types): ...


def start_bot() -> Any:
    """Function for start telegram bot"""
    return bot.infinity_polling()
