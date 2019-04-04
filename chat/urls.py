from django.urls import path

from chat.views import RoomListView, RoomDetailView
# , AjaxMessagesView

app_name = 'chat'

urlpatterns = [
    path('rooms/', RoomListView.as_view(), name='rooms'),
    path('room/<int:room_id>', RoomDetailView.as_view(), name = 'room'),
    # path('api/messages/<int:room_id>', AjaxMessagesView.as_view())
]
