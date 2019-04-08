import json
import asyncio
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.layers import get_channel_layer

from django.core.cache import cache

from chat.models import Message, Room

class CommonRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        room = Room.objects.get(id = self.room_id)
        user = self.scope["user"]
        if (user in room.all_members()):
            self.room_group_name = 'chat_%s' % (self.room_id)
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            cache_key = 'chat_%s_user_%s' % (self.room_id, user.id)
            cache.delete(cache_key)
            cache.add(cache_key, self.channel_name, 999999999)
        else:
            await self.close()   

    async def disconnect(self, close_code):
         await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['command'] == 'create_message':
            text_message = data['message']
            await self.create_message(text_message)
        elif data['command'] == 'get_messages':
            counter = data['counter']
            await self.get_messages_portion(counter)

    @database_sync_to_async
    def create_message(self, text_message):
        room = Room.objects.get(id = self.room_id)
        user = self.scope["user"]
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
                    'new_message': message.message_pack(),
                }
            )
 
    async def transmit_message(self, event):
        message = event['new_message']
        await self.send(text_data=json.dumps({
            'new_message': message,
        }))

    @database_sync_to_async
    def get_messages_portion(self, counter):
        room = Room.objects.get(id = self.room_id)
        user = self.scope["user"]
        border = counter + 5
        messages = room.all_messages()[counter : border]
        messages_pack = list()
        for message in messages:
            this_pack = message.packed_dict(user)
            messages_pack.append(this_pack)
        # cache_key = 'chat_%s_user_%s' % (self.room_id, user.id)
        # channel_layer = get_channel_layer()
        # my_channel_name = cache.get(cache_key)
        async_to_sync(self.channel_layer.send)(
            self.channel_name,
                {
                    'type': 'load_messages',
                    'messages_portion': messages_pack,
                    'counter': border
                }
        )

    async def load_messages(self, event):
        messages = event['messages_portion']
        counter = event['counter']
        await self.send(text_data=json.dumps({
            'messages_portion': messages,
            'counter': counter
        }))


# class ReadMessagesConsumer(AsyncWebsocketConsumer):

#     async def connect(self):
#         self.room_id = self.scope['url_route']['kwargs']['room_id']
#         self.room_group_name = 'reading_%s' % self.room_id
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()


#     async def disconnect(self, close_code):
#          await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         self.room_id = self.scope['url_route']['kwargs']['room_id']
#         data_json = json.loads(text_data)
#         counter = data_json['counter']  
#         room = Room.objects.get(id = self.room_id)
#         user = self.scope["user"]
#         await self.read_this_messages(room, counter, user)      

#     @database_sync_to_async
#     def read_this_messages(self, room, counter, user):
#         all_messages = room.all_messages()[: counter]
#         updating_messages = list()
#         for m in all_messages:
#             if m.has_not_user_read(user):
#                 updating_messages.append(m)
#         updated_pack = list() 
#         for message in updating_messages:
#             message.had_read.add(user)
#             message.save()   
#             if (message.white_message_for_user(user)):
#                 updated_pack.append(message.id)
#         async_to_sync(self.channel_layer.group_send)(
#                 self.room_group_name,
#                 {
#                     'type': 'return_updated',
#                     'updated': updated_pack,
#                 }
#             )

#     async def return_updated(self, event):
#         updated = event['updated']
#         await self.send(text_data=json.dumps({
#             'updated': updated,
#         }))
