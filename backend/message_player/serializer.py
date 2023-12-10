from rest_framework import serializers

from message_player.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "message", "created_at")
