# from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from chat.models import Room
from django.shortcuts import get_object_or_404


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
