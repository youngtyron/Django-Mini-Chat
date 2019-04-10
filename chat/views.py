from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from chat.models import Room, MessageImage
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


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