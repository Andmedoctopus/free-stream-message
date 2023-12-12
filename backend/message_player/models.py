from django.db import models
from django.conf import settings

class Message(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
       settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )

    def __str__(self):
        return self.message
