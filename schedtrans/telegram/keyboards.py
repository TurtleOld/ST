from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from schedtrans.telegram.common import SentMessage, prepare_json_file_route
from schedtrans.telegram.config import bot


async def select_transport_type(message: types.Message) -> None:
    keyboard = InlineKeyboardMarkup(row_width=1)
    bus = InlineKeyboardButton(
        '\u00A0\u00A0Автобус\u00A0\u00A0',
        callback_data='bus',
    )
    suburban = InlineKeyboardButton(
        '\u00A0\u00A0Электричка\u00A0\u00A0',
        callback_data='suburban',
    )
    keyboard.add(bus, suburban)
    sent_message = await bot.send_message(
        message.chat.id,
        '\u00A0\u00A0Выбери тип транспорта\u00A0\u00A0',
        reply_markup=keyboard,
    )
    SentMessage.send_message.append(sent_message)


async def selected_transport_type(message: types.Message, call_data) -> None:
    keyboard = InlineKeyboardMarkup(row_width=2)
    json_route = prepare_json_file_route()
    for key, value in json_route.items():
        name_route = value.get('name_route', None)
        transport_types = value.get('transport_types', None)
        if (
            call_data == 'bus'
            and transport_types == 'bus'
            or call_data == 'suburban'
            and transport_types == 'suburban'
        ):
            keyboard.row(
                InlineKeyboardButton(
                    text=f'\u00A0\u00A0{name_route}\u00A0\u00A0',
                    callback_data=f'{key}',
                )
            )
    keyboard.add(
        InlineKeyboardButton(
            text='Вернуться в начало',
            callback_data='back',
        )
    )
    sent_message = await bot.send_message(
        message.chat.id,
        'Выбери направление',
        reply_markup=keyboard,
        parse_mode='HTML',
    )
    SentMessage.send_message.append(sent_message)


async def selected_route(message, json_route, transport_type):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for key, value in json_route.items():
        tp_types = value.get('transport_type', None)
        if tp_types == transport_type:
            number = value.get('number', None)
            short_title = value.get('short_title', None)
            departure_format_date = value.get('departure_format_date', None)
            duration = value.get('duration', None)
            text_button = '{} | {} ({}) | {}'.format(
                number,
                departure_format_date,
                duration,
                short_title,
            )
            keyboard.row(
                InlineKeyboardButton(
                    text=f'\u00A0\u00A0{text_button}\u00A0\u00A0',
                    callback_data=key,
                ),
            )
    keyboard.add(
        InlineKeyboardButton(
            text='Вернуться в начало',
            callback_data='back',
        )
    )
    sent_message = await bot.send_message(
        message.chat.id,
        'Выбери маршрут:',
        reply_markup=keyboard,
        parse_mode='HTML',
    )
    SentMessage.send_message.append(sent_message)


async def back_main(message: types.Message, threads: str) -> None:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text='Вернуться в начало',
            callback_data='back',
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text='Запомнить маршрут',
            callback_data=f'schedule_{message.chat.id}',
        )
    )
    sent_message = await bot.send_message(
        message.chat.id,
        threads,
        reply_markup=keyboard,
    )
    SentMessage.send_message.append(sent_message)


async def back_from_routes(message: types.Message, routes: str) -> None:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text='Вернуться в начало',
            callback_data='back',
        )
    )
    sent_message = await bot.send_message(
        message.chat.id,
        routes,
        reply_markup=keyboard,
    )
    SentMessage.send_message.append(sent_message)
