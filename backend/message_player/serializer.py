from message_player.models import Message
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Message
        fields = ("id", "message", "created_at")
