from django.core.management.base import BaseCommand, CommandError
from API.models import OnlineUser

from datetime import datetime

class Command(BaseCommand):
    help = 'Removes all away players'
    maxAwayTime = 600 # 10 minutes

    def handle(self, *args, **options):
        users = OnlineUser.objects.all()
        for user in users:
            user_time = user.lastActivity.replace(tzinfo=None)
            cur_time = datetime.utcnow()
            delta_seconds = (cur_time-user_time).total_seconds()
            if delta_seconds > self.maxAwayTime:
                user.delete()



        