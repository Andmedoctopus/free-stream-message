from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/message", views.send_message, name="send_message"),
]
