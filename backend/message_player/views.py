from django.shortcuts import render
import channels.layers
from django.http import HttpResponse
from asgiref.sync import async_to_sync
from django.views.decorators.http import require_http_methods
import json
# Create your views here.
def index(request):
    return render(request, "index.html")

@require_http_methods(["POST"])
def send_message(request):
    body =json.loads(request.body)
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "message", {"type": "chat.message", "message": body["message"]}
    )
    return HttpResponse('')
