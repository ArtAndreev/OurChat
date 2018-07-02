from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_room_group'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    # async def receive(self, text_data):
        # message = json.loads(text_data)
        #
        #
        # # Send message to room group
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': message
        #     }
        # )
        # pass

    async def send_message(self, text_data=None, bytes_data=None, close=False):
        message = text_data['message']
        attachments = text_data['attachments']
        if not attachments:
            send_message = json.dumps({
                'id': message.id,
                'text': message.text,
                'date': message.date
            })
        else:
            send_message = json.dumps({
                'id': message.id,
                'text': message.text,
                'date': message.date,
                'attaches': attachments
            })
        super().send()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': send_message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['send_message']

        # Send message to WebSocket
        await self.send(text_data=message)
