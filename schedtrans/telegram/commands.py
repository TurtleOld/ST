from typing import Any

from icecream import ic
from telebot import types

from schedtrans.json_request.request import RequestSchedule
from schedtrans.prepare_data.process_data_generate import Processing
from schedtrans.telegram.common import (
    SentMessage,
    prepare_json_file_route,
)
from schedtrans.telegram.config import bot
from schedtrans.telegram.keyboards import (
    select_transport_type,
    selected_transport_type,
    selected_route,
    back_from_routes,
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
    @bot.callback_query_handler(
        func=lambda call: call.data
        in [
            'bus',
            'suburban',
        ]
    )
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
        sent_message = await bot.send_message(
            call.message.chat.id,
            'Загружается...',
        )

        ic(sent_message)
        SentMessage.send_message.append(sent_message)
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
                CallBackQueryHandlerTransportType.result_json_route = thread_json_data
                await selected_route(
                    message=call.message,
                    json_route=thread_json_data,
                    transport_type=transport_type,
                )
        await bot.delete_message(
            call.message.chat.id,
            SentMessage.send_message[-2].message_id,
        )

    @staticmethod
    @bot.callback_query_handler(
        func=lambda call: call.data in 'back',
    )  # type: ignore
    async def come_back_main(call: types.CallbackQuery) -> None:
        for message in SentMessage.send_message:
            try:
                await bot.delete_message(
                    call.message.chat.id,
                    message.message_id,
                )
            except Exception as e:
                print(e)
                continue
        CallBackQueryHandlerTransportType.result_json_route.clear()
        await select_transport_type(call.message)

    @staticmethod
    @bot.callback_query_handler(func=lambda call: True)
    async def callback_handle_detail_transport(call: types.CallbackQuery) -> None:
        await bot.delete_message(call.message.chat.id, call.message.id)
        result_detail_transport = ''
        for key, value in CallBackQueryHandlerTransportType.result_json_route.items():
            if call.data == key:
                transport_type = value.get('transport_type')
                number = value.get('number')
                short_title = value.get('short_title')
                days = value.get('days')
                duration = value.get('duration')
                departure_format_date = value.get('departure_format_date')
                arrival_format_date = value.get('arrival_format_date')
                to_station = value.get('to_station').get('title')
                stops = value.get('stops')
                if stops == '':
                    stops = 'Везде'
                transport_type_name = 'Электричка'
                if transport_type == 'bus':
                    transport_type_name = 'Автобус'
                result_detail_transport += '<strong>{}:</strong> #{} {}\n'.format(
                    transport_type_name,
                    number,
                    short_title,
                )
                result_detail_transport += (
                    '<strong>Отправляется в:</strong> {}\n'.format(
                        departure_format_date
                    )
                )
                result_detail_transport += (
                    '<strong>График движения:</strong> {}\n'.format(days)
                )
                result_detail_transport += (
                    '<strong>С остановками:</strong> {}\n'.format(stops)
                )
                result_detail_transport += '<strong>Время в пути:</strong> {}\n'.format(
                    duration
                )
                result_detail_transport += (
                    '<strong>Приезжает в пункт назначения {} в {}</strong>'.format(
                        to_station, arrival_format_date
                    )
                )
        await back_from_routes(call.message, result_detail_transport)


def start_bot() -> Any:
    """Function for start telegram bot"""
    return bot.infinity_polling()
