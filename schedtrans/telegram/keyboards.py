import json
import os

from icecream import ic
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from schedtrans.telegram.common import SentMessage
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
    current_directory = os.path.dirname(__file__)
    file_name = 'routes.json'
    file_path = os.path.abspath(os.path.join(current_directory, file_name))
    with open(file_path, 'r') as route_file:
        json_route = json.load(route_file)
    for key, value in json_route.items():
        if (
            call_data == 'bus'
            and value.get('transport_types') == 'bus'
            or call_data == 'suburban'
            and value.get('transport_types') == 'suburban'
        ):
            keyboard.row(
                InlineKeyboardButton(
                    text=value.get('name_route'),
                    callback_data=f'{key}',
                )
            )
    sent_message = await bot.send_message(
        message.chat.id,
        'Выбери направление',
        reply_markup=keyboard,
        parse_mode='HTML',
    )
    SentMessage.send_message.append(sent_message)
