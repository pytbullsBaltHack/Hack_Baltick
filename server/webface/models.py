from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class StreamSource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    camera_source = models.CharField(max_length=100, default='-1')
    date = models.DateTimeField(default=timezone.now)
    is_run = models.IntegerField(default=0)
    event = models.IntegerField(default=0)

    def __str__(self):
        return self.camera_source


class UserFace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    face_id = models.CharField(max_length=5000, default='')
    img = models.CharField(max_length=200, default='')
    name = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.face_id


class Visitor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    face_id = models.CharField(max_length=5000, default='')
    date = models.DateTimeField(default=timezone.now)
    fake_user_id = models.CharField(max_length=5000, default='')
    event = models.IntegerField(default=0)

    def __str__(self):
        return self.face_id


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    name = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name
