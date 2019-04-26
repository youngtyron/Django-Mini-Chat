import json
import asyncio
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.contrib.auth.models import User
from chat.models import Message, Room, MessageImage

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
            images_id_list = data['images']            
            await self.create_message(text_message, images_id_list)
        elif data['command'] == 'get_messages':
            counter = data['counter']
            await self.get_messages_portion(counter)
        elif data['command'] == 'read_messages':
            counter = data['counter']
            await self.read_messages(counter)
        elif data['command'] == 'typing':
            await self.typing_translate()
        elif data['command'] == 'stoptyping':
            await self.stoptyping_translate()
        elif data['command'] == 'new_member':
            potential_id = data['potential_id']
            await self.add_new_member(potential_id)
        elif data['command'] == 'leave_chat':
            await self.leave_chat()

    @database_sync_to_async
    def create_message(self, text_message, images_id_list):
        room = Room.objects.get(id = self.room_id)
        user = self.scope["user"]
        message = Message.objects.create(author = user,
                               room = room,
                               text = text_message
            )
        if images_id_list:
            for image_id in images_id_list:
                image = MessageImage.objects.get(id = image_id)
                message.image.add(image)
        message.had_read.add(user)
        message.save()
        for addressee in room.all_members():
            cache_key = 'chat_%s_user_%s' % (self.room_id, addressee.id)
            addressee_channel_name = cache.get(cache_key)
            if addressee_channel_name != None:
                async_to_sync(self.channel_layer.send)(
                    addressee_channel_name,
                        {
                            'type': 'transmit_message',
                            'new_message': message.packed_dict(addressee),
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

    @database_sync_to_async
    def read_messages(self, counter):
        room = Room.objects.get(id = self.room_id)
        all_messages = room.all_messages()[: counter]
        updating_messages = list()
        user = self.scope["user"]
        for m in all_messages:
            if m.has_not_user_read(user):
                updating_messages.append(m)
        distribution_list = list()
        for member in room.all_members():
            if self.belong_to_distribution_list(updating_messages, member):
                distribution_list.append(member)
        for message in updating_messages:
            message.had_read.add(user)
            message.save()   
        for addressee in distribution_list:
            distributed_data = list()
            for updating_message in updating_messages:
                distributed_data.append({'id': updating_message.id, 'not_read': updating_message.green_message_for_user(addressee), 
                                         'need_update': updating_message.need_read_and_update(addressee)})
            cache_key = 'chat_%s_user_%s' % (self.room_id, addressee.id)
            addressee_channel_name = cache.get(cache_key)
            async_to_sync(self.channel_layer.send)(
                addressee_channel_name,
                    {
                        'type': 'return_read',
                        'updated_messages': distributed_data,
                    }
            )

    def belong_to_distribution_list(self, messages, user):
        for message in messages:
            if message.green_message_for_user(user):
                return True 
        return False

    
    async def return_read(self, event):
        updated_messages = event['updated_messages']
        await self.send(text_data=json.dumps({
            'updated_messages': updated_messages
        }))

    async def typing_translate(self):
        user = self.scope["user"]
        await self.channel_layer.group_send(
            self.room_group_name,
                {
                    'type': 'return_typing',
                    'user_data': str(user.first_name)+' '+str(user.last_name),               
                }
        )

    async def return_typing(self, event):
        user_data = event['user_data']
        await self.send(text_data=json.dumps({
            'user_is_typing': user_data,
        }))

    async def stoptyping_translate(self):
        user = self.scope["user"]
        await self.channel_layer.group_send(
            self.room_group_name,
                {
                    'type': 'return_stoptyping',
                    'user_data': str(user.first_name)+' '+str(user.last_name),               
                }
        )

    async def return_stoptyping(self, event):
        user_data = event['user_data']
        await self.send(text_data=json.dumps({
            'user_stopped_typing': user_data,
        }))

    async def return_become_online(self, event):
        user_data = event['user_data']
        await self.send(text_data=json.dumps({
            'user_become_online': user_data,
        }))

    async def return_become_offline(self, event):
        user_data = event['user_data']
        await self.send(text_data=json.dumps({
            'user_become_offline': user_data,
        }))

    @database_sync_to_async
    def add_new_member(self, potential_id):
        room = Room.objects.get(id = self.room_id)
        user = self.scope["user"]
        new_member = get_object_or_404(User, id = potential_id)
        room.member.add(new_member)
        room.save()
        new_member_dict = new_member.chatprofile.user_dict()
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
                {
                    'type': 'return_new_member',
                    'new_member_data': new_member_dict,               
                }
        )

    async def return_new_member(self, event):
        new_member_data = event['new_member_data']
        await self.send(text_data=json.dumps({
            'new_member': new_member_data,
        }))

    @database_sync_to_async
    def leave_chat(self):
        room = Room.objects.get(id = self.room_id)
        user = self.scope["user"]
        room.member.remove(user)
        user_data = user.chatprofile.user_dict()
        for member in room.all_members():

            cache_key = 'chat_%s_user_%s' % (self.room_id, member.id)
            addressee_channel_name = cache.get(cache_key)
            async_to_sync(self.channel_layer.send)(
                addressee_channel_name,
                    {
                        'type': 'return_leave_chat',
                        'user_data': user_data,
                    }
            )      

    async def return_leave_chat(self, event):
        user_data = event['user_data']
        await self.send(text_data=json.dumps({
            'leave_chat': user_data,
        }))