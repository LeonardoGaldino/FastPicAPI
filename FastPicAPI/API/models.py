from __future__ import unicode_literals

from django.db import models


class OnlineUser(models.Model):
    name = models.CharField(unique=True, max_length=120)
    points = models.IntegerField()


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=120, unique=True)
    owner_name = models.CharField(max_length=120)
    participants = models.ManyToManyField(OnlineUser)
