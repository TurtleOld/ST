import asyncio

from blacksheep import post, Request
from telebot import types

from schedtrans.telegram.commands import (
    CallBackQueryHandlerTransportType,
    handler_command_request,
    start_command_bot,
)
from schedtrans.telegram.config import bot

bot.add_message_handler(start_command_bot)
bot.add_message_handler(handler_command_request)
bot.add_callback_query_handler(
    CallBackQueryHandlerTransportType.callback_handle_transport_type,
)
bot.add_callback_query_handler(
    CallBackQueryHandlerTransportType.callback_handle_transport_route,
)
bot.add_callback_query_handler(
    CallBackQueryHandlerTransportType.callback_handle_detail_transport,
)
bot.add_callback_query_handler(CallBackQueryHandlerTransportType.come_back_main)


@post('/webhooks')
async def webhooks(request: Request) -> None:
    json_data = await request.json()
    update = types.Update.de_json(json_data)
    asyncio.ensure_future(bot.process_new_updates([update]))
