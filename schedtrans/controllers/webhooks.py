from blacksheep.server.controllers import Controller, get


class WebhookController(Controller):
    @get('/webhooks')
    def webhooks(self):
        return self.ok()
