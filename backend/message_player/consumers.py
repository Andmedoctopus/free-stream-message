import json

from channels.generic.websocket import AsyncWebsocketConsumer


class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("message", self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        print("in receive")
        pass

    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
