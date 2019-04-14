from django.urls import path
from chat import views
from chat.views import RoomListView, RoomDetailView

app_name = 'chat'

urlpatterns = [
    path('rooms/', RoomListView.as_view(), name='rooms'),
    path('room/<int:room_id>', RoomDetailView.as_view(), name = 'room'),
    path('send_message_images/<int:room_id>/', views.ajax_images_sending),
	path('get_users/<int:room_id>/', views.ajax_get_users),
]
