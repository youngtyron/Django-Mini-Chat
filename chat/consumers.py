import json
import asyncio
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import Message, Room

class NewMessagesConsumer(AsyncWebsocketConsumer):

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

    @database_sync_to_async
    def create_message(self, user, text_message):
        room = Room.objects.get(id = self.room_id)
        message = Message.objects.create(author = user,
                               room = room,
                               text = text_message
            )
        message.had_read.add(user)
        message.save()
        async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'transmit_message',
                    'message': message.message_pack()
                }
            )

    async def transmit_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

class MessagePortionConsumer(AsyncWebsocketConsumer):


    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        user = self.scope["user"]
        room = Room.objects.get(id = self.room_id)
        if (user in room.all_members()):
            self.room_group_name = 'chat_%s_user_%s' % (self.room_id, user.id)
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            self.close()        


    async def disconnect(self, close_code):
         await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        room = Room.objects.get(id = self.room_id)
        data_json = json.loads(text_data)
        counter = data_json['counter']
        await self.get_messages_portion(room, counter)

    @database_sync_to_async
    def get_messages_portion(self, room, counter):
        border = counter + 5
        messages = room.all_messages()[counter : border]
        messages_pack = list()
        for message in messages:
            messages_pack.append(message.message_pack())
        async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'load_messages',
                    'messages': messages_pack,
                    'counter': border
                }
            )

    async def load_messages(self, event):
        messages = event['messages']
        counter = event['counter']
        await self.send(text_data=json.dumps({
            'messages': messages,
            'counter': counter
        }))