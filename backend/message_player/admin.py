from django.contrib import admin
from message_player.models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ("message", "created_at")


admin.site.register(Message, MessageAdmin)
