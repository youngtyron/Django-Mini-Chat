from django.urls import path
from chat import views
from chat.views import AllRoomsView, RoomDetailView, NewRoomView

app_name = 'chat'

urlpatterns = [
    path('rooms/', AllRoomsView.as_view(), name='rooms'),
    path('room/<int:room_id>', RoomDetailView.as_view(), name = 'room'),
    path('new_room', NewRoomView.as_view(), name = 'new_room'),
    path('send_message_images/<int:room_id>/', views.ajax_images_sending),
	path('get_users/<int:room_id>/', views.ajax_get_users),
	path('get_rooms/', views.ajax_get_rooms),
	path('search_users/', views.ajax_search_users),
	path('create_chat/', views.ajax_create_chat),
]
