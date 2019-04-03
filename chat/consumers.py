import json
import asyncio
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import Message, Room

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_id

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
         await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text_message = text_data_json['message']
        user = self.scope["user"]
        await self.create_message(user, text_message)
        print('receive')
        await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': text_message
                }
            )

    @database_sync_to_async
    def create_message(self, user, text_message):
        room = Room.objects.get(id = self.room_id)
        print('create')
        message = Message.objects.create(author = user,
                               room = room,
                               text = text_message
            )
        message.had_read.add(user)
        message.save()

    async def chat_message(self, event):
        print('to_chat')
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))






