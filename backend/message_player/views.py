import json

import channels.layers
from asgiref.sync import async_to_sync
from django.contrib.messages import Message
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets

from message_player.models import Message
from message_player.serializer import MessageSerializer


# Create your views here.
def index(request):
    return render(request, "index.html")


@require_http_methods(["POST"])
def send_message(request):
    body = json.loads(request.body)
    async_to_sync(channel_layer.group_send)(
        "message", {"type": "chat.message", "message": body["message"]}
    )
    return HttpResponse("")


channel_layer = channels.layers.get_channel_layer()


class MessageView(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request):
        response = super().create(request)

        message = response.data["message"]

        async_to_sync(channel_layer.group_send)(
            "message", {"type": "chat.message", "message": message}
        )
        return response
