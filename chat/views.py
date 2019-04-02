from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from chat.models import Room, Message, MessageImage
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse


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

class AjaxMessagesView(View):
	room = None
	messages = None

	def dispatch(self, request, *args, **kwargs):
		if not request.is_ajax():
			return HttpResponse("Http method is disabled", status=405)
		user = self.request.user
		self.room = get_object_or_404(Room, id = self.kwargs['room_id'])
		if not user in self.room.all_members():
			return HttpResponse(status=403)
		self.messages = Message.objects.filter(room = self.room)
		return super(AjaxMessagesView, self).dispatch(request, *args, **kwargs)

	def get(self, request, *args, **kwargs):
		raw_pack = list()
		for message in self.messages:
			raw_pack.append(message.message_pack())
		return JsonResponse(raw_pack, safe=False)