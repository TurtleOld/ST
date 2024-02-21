import json
import os
from typing import Any

from icecream import ic
from telebot import types

from schedtrans.json_request.request import RequestSchedule
from schedtrans.prepare_data.process_data_generate import Processing
from schedtrans.telegram.common import (
    SentMessage,
    prepare_json_file_route,
    get_thread_json_data,
)
from schedtrans.telegram.config import bot
from schedtrans.telegram.keyboards import (
    select_transport_type,
    selected_transport_type,
    selected_route,
)


@bot.message_handler(commands=['start'])
async def start_command_bot(message):
    await bot.send_message(message.chat.id, 'Бот запущен!')


@bot.message_handler(commands=['select'])  # type: ignore
async def handler_command_request(message: types.Message) -> None:
    await select_transport_type(message)


class CallBackQueryHandlerTransportType:
    result_json_route = {}

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
        result = []
        for key in json_route:
            result.append(key)
        return result

    @staticmethod
    @bot.callback_query_handler(
        func=lambda call: call.data in [key for key in prepare_json_file_route()],
    )
    async def callback_handle_transport_route(call: types):
        await bot.delete_message(call.message.chat.id, call.message.id)
        json_route = prepare_json_file_route()
        for key, value in json_route.items():
            if call.data == key:
                transport_type = value.get('transport_types')
                prepare_request = RequestSchedule(
                    from_station=value.get('from_station'),
                    to_station=value.get('to_station'),
                    transport_types=transport_type,
                )
                result_request = (
                    await prepare_request.request_transport_between_stations()
                )
                process_json_data = Processing(result_request.json())
                await process_json_data.detail_route()
                thread_json_data = await process_json_data.detail_thread()
                await selected_route(
                    message=call.message,
                    json_route=thread_json_data,
                    transport_type=transport_type,
                )
                get_thread_json_data(thread_json_data)


def start_bot() -> Any:
    """Function for start telegram bot"""
    return bot.infinity_polling()
