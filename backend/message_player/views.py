import channels.layers
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from asgiref.sync import async_to_sync
from django.contrib.messages import Message
from django.shortcuts import render
from message_player.models import Message
from message_player.serializer import MessageSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets, mixins

from rest_framework import status

def index(request):
    return render(request, "index.html")


channel_layer = channels.layers.get_channel_layer()


class MessageView(
        APIView
):
    #serializer_class = MessageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=MessageSerializer, responses={201: MessageSerializer(many=False), 401: "Validation error"})
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            breakpoint()
            serializer.save()

            #message = response.data["message"]

            #async_to_sync(channel_layer.group_send)(
            #    "message", {"type": "chat.message", "message": message}
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST

        )
