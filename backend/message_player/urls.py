from django.urls import include, path
from rest_framework import routers

from message_player import views

router = routers.DefaultRouter()
router.register(r"messages", views.MessageView, "message")


urlpatterns = [
    path("", views.index, name="index"),
    path("api/", include(router.urls)),
    path("api/message", views.send_message, name="send_message"),
]
