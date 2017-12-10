from __future__ import unicode_literals

from django.db import models

class OnlineUser(models.Model):
    name = models.CharField(unique=True, max_length=120)
    points = models.IntegerField()

# This table will save the name of the player who got the highest number of points
# And also the number of points
# This table should have only one entry!
class Rank(models.Model):
    name = models.CharField(unique=True, max_length=120)
    points = models.IntegerField()