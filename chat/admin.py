from django.contrib import admin
from .models import ChatRoom, ChatMessage

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'created_at')
    list_display_links = ('id', 'listing',)
    filter_horizontal = ('participants',)  

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_room', 'sender', 'timestamp')
    list_display_links = ('id', 'chat_room',)
    list_filter = ('timestamp',)
    search_fields = ('message',)
