from uuid import uuid4
from django.db import models
from identities.models import Identity


class Chat(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    identity = models.ForeignKey(Identity, on_delete=models.SET_NULL, blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.id}"


class Message(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    chat = models.ForeignKey(Chat, null=False, blank=False, on_delete=models.CASCADE)
    message = models.TextField(null=False, blank=False)
    role = models.CharField(max_length=200, choices=(
        ('system', 'System'),
        ('assistant', 'Assistant'),
        ('user', 'user')
    ))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    objects = models.Manager()

    def __str__(self):
        return f"{self.message} | {self.chat.id}"
