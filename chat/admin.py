from django.contrib import admin
from chat.models import Room, Message, MessageImage, ChatProfile
# Register your models here.
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(MessageImage)
admin.site.register(ChatProfile)