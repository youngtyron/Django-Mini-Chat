from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from chat.models import Room, MessageImage
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.cache import cache
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.auth.models import User

class AllRoomsView(TemplateView, LoginRequiredMixin):
	template_name = 'room_list.html'

class NewRoomView(TemplateView, LoginRequiredMixin):
	template_name = 'new_room.html'


@login_required
def room_list(request, room_id):
	room = get_object_or_404(Room, id = room_id)
	if request.user in room.all_members():
		return render(request, 'messages_list.html', {'id': room_id})
	else:
		return HttpResponseRedirect('/chat/rooms/')

@login_required
def ajax_images_sending(request, room_id):
	if request.method == 'POST' and request.is_ajax:
		room = get_object_or_404(Room, id = room_id)
		images = request.FILES.getlist('images-input')
		id_list = list()
		for image in images:
			pict = MessageImage.objects.create(room = room, image = image)
			id_list.append(pict.id)
		return JsonResponse({'id_list':id_list})

@login_required
def ajax_get_users(request, room_id):
	if request.is_ajax:
		room = get_object_or_404(Room, id = room_id)
		users = room.all_members()
		if not request.user in users:
			return HttpResponse(403)
		users_list = list()
		for user in users:
			online = cache.get('user_online_' + str(user.id))
			user_dict = {'first_name': user.first_name, 
						'last_name': user.last_name, 
						'online': online, 
						'id': user.id,
						'avatar': user.chatprofile.avatar_url()}
			users_list.append(user_dict)
		return JsonResponse({'users': users_list})


@login_required
def ajax_get_rooms(request):
	if request.is_ajax:
		rooms = Room.objects.filter(member = request.user)
		rooms_list = list()
		for room in rooms:
			room_dict = {'id': room.id, 
	    				 'title_name': room.title_name(),
	    				 'all_members': room.all_members_list(), 
	    				 'last_message_title': room.last_message_title(request.user)
			}
			rooms_list.append(room_dict)
		return JsonResponse({'rooms': rooms_list})

@login_required
def ajax_search_users(request):
	if request.is_ajax:
		searchText = request.POST['search']
		matched_users = User.objects.filter(Q(first_name__contains = searchText) | Q (last_name__contains = searchText)).exclude(id = request.user.id)
		users_list = list()
		for user in matched_users:
			users_list.append(user.chatprofile.user_dict())
		return JsonResponse({'matched_users': users_list})

@login_required
def ajax_potential_members(request, room_id):
	if request.is_ajax:
		room = get_object_or_404(Room, id = room_id)
		searchMember = request.POST['search']
		matched = User.objects.filter(Q(first_name__contains = searchMember) | Q (last_name__contains = searchMember)).exclude(id = request.user.id)
		potential_members = list()
		for m in matched:
			if m not in room.all_members():
				potential_members.append(m.chatprofile.user_dict())
		return JsonResponse({'potential_members': potential_members})

@login_required
def ajax_create_chat(request):
	if request.is_ajax:
		room = Room.objects.create()
		id_list = request.POST['ids'].split(',')
		for one_id in id_list:
			member = get_object_or_404(User, id = one_id)
			room.member.add(member)
		room.member.add(request.user)
		return JsonResponse({'room_id': room.id})