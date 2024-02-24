import json

from blacksheep import post, Request
from telebot import types

from schedtrans.telegram.config import bot


@post('/webhooks')
async def webhooks(request: Request) -> None:
    if request.method == 'POST':
        json_request = await request.json()
        print(json_request)
        # json_data = json.loads(json_request)
        # update = types.Update.de_json(json_data)
        # bot.process_new_updates([update])
