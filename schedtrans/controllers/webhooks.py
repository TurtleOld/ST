import asyncio

from blacksheep import post, Request
from telebot import types

from schedtrans.telegram.config import bot


@post('/webhooks')
async def webhooks(request: Request) -> None:
    if request.method == 'POST':
        json_data = await request.json()
        update = types.Update.de_json(json_data)
        asyncio.ensure_future(bot.process_new_updates([update]))
