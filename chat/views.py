from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from chat.models import Room, MessageImage
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.cache import cache
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from chat.consumers import CommonRoomConsumer

class RoomListView(ListView):
	template_name = 'room_list.html'
	model = Room

	def get_queryset(self):
		rooms = Room.objects.filter(member = self.request.user)
		return rooms

class RoomDetailView(DetailView):
	template_name = 'messages_list.html'

	def get_object(self, **kwargs):
		obj = get_object_or_404(Room, id = self.kwargs['room_id'])
		return obj

def ajax_images_sending(request, room_id):
	if request.method == 'POST' and request.is_ajax:
		room = get_object_or_404(Room, id = room_id)
		images = request.FILES.getlist('images-input')
		id_list = list()
		for image in images:
			pict = MessageImage.objects.create(room = room, image = image)
			id_list.append(pict.id)
		return JsonResponse({'id_list':id_list})

def ajax_get_users(request, room_id):
	if request.is_ajax:
		room = get_object_or_404(Room, id = room_id)
		users = room.all_members()
		if not request.user in users:
			return HttpResponse(403)
		users_list = list()
		for user in users:
			online = cache.get('user_online_' + str(user.id))
			user_dict = {'first_name': user.first_name, 'last_name': user.last_name, 'online': online, 'id': user.id}
			users_list.append(user_dict)
		return JsonResponse({'users': users_list})


def become_online_chat_announcement(user):
    rooms = Room.objects.filter(member = user)
    user_data = {'online': True, 'id': user.id}
    channel_layer = get_channel_layer()				
    for room in rooms:
        room_group_name = 'chat_%s' % (room.id)
        async_to_sync(channel_layer.group_send)(
            room_group_name,
                {
                    'type': 'return_become_online',
                    'user_data': user_data,                  
                }
        )
    return

def become_offline_chat_announcement(user):
    rooms = Room.objects.filter(member = user)
    user_data = {'online': False, 'id': user.id}
    channel_layer = get_channel_layer()				
    for room in rooms:
        room_group_name = 'chat_%s' % (room.id)
        async_to_sync(channel_layer.group_send)(
            room_group_name,
                {
                    'type': 'return_become_offline',
                    'user_data': user_data,                  
                }
        )
    return 