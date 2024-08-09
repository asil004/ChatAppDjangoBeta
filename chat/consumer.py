import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from chat.db_commands import get_or_create_user, get_or_create_chat_room, get_messages, message_create, \
    get_user_from_jwt

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.chat_room = None
        self.room_group_name = None
        self.room_name = None
        self.user_sender = None

    async def connect(self):
        token = None
        for header in self.scope['headers']:
            if header[0] == b'authorization':
                token = header[1].decode().split(' ')[1]
                break

        # Decode the token and get the user
        self.user_sender = await get_user_from_jwt(token)
        self.room_name = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f"chat_{self.room_name}"
        self.user, _ = await get_or_create_user(self.room_name)
        self.chat_room, _ = await get_or_create_chat_room(self.user)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        messages = await get_messages(room=self.chat_room)
        # message_json = json.dumps(messages)

        await self.accept()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': messages
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await message_create(room=self.chat_room, author=self.user_sender, message=message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
