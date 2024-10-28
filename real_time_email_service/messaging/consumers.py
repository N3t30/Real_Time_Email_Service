import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            await self.channel_layer.group_add(f"user_{self.user.id}", self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(f"user_{self.user.id}", self.channel_name)

    async def send_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

#  O código define uma classe NotificationConsumerpara gerenciar conexões WebSocket com autenticação de usuários.
# Ele adiciona o usuário autenticado a um grupo específico e permite o envio de notificações.
# Minha primeira experiencia com WebSocket.
