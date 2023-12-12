from django.urls import include, path
from message_player import views
from rest_framework import routers

urlpatterns = [
    path("", views.index, name="index"),
    path("api/v1/messages", views.MessageView.as_view()),
]
