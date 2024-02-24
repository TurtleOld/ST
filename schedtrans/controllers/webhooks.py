import json
from blacksheep.server.controllers import Controller, post
from telebot import types

from schedtrans.telegram.config import bot


class WebhookController(Controller):
    @post('/webhooks/')
    def webhooks(self, request) -> None:
        if request.method == 'POST':
            json_data = json.loads(request.body)
            update = types.Update.de_json(json_data)
            bot.process_new_updates([update])
