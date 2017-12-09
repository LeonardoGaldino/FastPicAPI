from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=120, unique=True)
    owner_name = models.CharField(max_length=120)


class OnlineUser(models.Model):
    name = models.CharField(unique=True, max_length=120)
    points = models.IntegerField()
