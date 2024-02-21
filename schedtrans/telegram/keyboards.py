import json
import os

from icecream import ic
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
    json_route = await prepare_json_file_route()
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
    sent_message = await bot.send_message(
        message.chat.id,
        'Выбери направление',
        reply_markup=keyboard,
        parse_mode='HTML',
    )
    SentMessage.send_message.append(sent_message)
