from blacksheep import json
from blacksheep.server.controllers import Controller, post
from icecream import ic


class WebhookController(Controller):
    @post('/webhooks')
    def webhooks(self, request):
        return request.method
