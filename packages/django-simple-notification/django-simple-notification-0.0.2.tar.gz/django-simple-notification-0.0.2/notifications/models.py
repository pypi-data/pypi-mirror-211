from django.db import models

from EasySell_backend import settings
from apps.utils.abstracts import TimeStampedModel


class Notification(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    content = models.TextField()
    type = models.CharField(max_length=100, null=True, blank=True)

    def to_json(self):
        return {
            'id': self.id,
            'is_read': self.is_read,
            'content': self.content,
            'user':
                {
                    'id': self.user.id,
                    'username': self.user.username
                },

        }
