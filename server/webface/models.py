from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class StreamSource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    camera_source = models.CharField(max_length=100, default='-1')
    date = models.DateTimeField(default=timezone.now)
    is_run = models.IntegerField(default=0)

    def __str__(self):
        return self.camera_source
