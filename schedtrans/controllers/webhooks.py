import asyncio

from blacksheep import post, Request
from icecream import ic
from telebot import types

from schedtrans.telegram.config import bot


@post('/webhooks')
async def webhooks(request: Request) -> None:
    json_data = await request.json()
    print(json_data)
    update = types.Update.de_json(json_data)
    asyncio.ensure_future(bot.process_new_updates([update]))
