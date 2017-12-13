from __future__ import unicode_literals

from django.db import models

from datetime import datetime

class OnlineUser(models.Model):
    name = models.CharField(unique=True, max_length=120)
    points = models.IntegerField()
    lastActivity = models.DateTimeField(auto_now=True)

    def updateLastActivity(self):
        self.lastActivity = datetime.now()
        self.save()

# This table will save the name of the player who got the highest number of points
# And also the number of points
# This table should have only one entry!
class Rank(models.Model):
    name = models.CharField(unique=True, max_length=120)
    points = models.IntegerField()

class PictureTarget(models.Model):
    name = models.CharField(max_length=120)
    nextChange = models.DateTimeField(auto_now=True)