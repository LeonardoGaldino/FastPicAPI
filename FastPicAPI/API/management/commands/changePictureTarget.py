from django.core.management.base import BaseCommand, CommandError
from API.models import PictureTarget
from random import randint

pictureNames = ['pen', 'notebook', 'pencil', 'mouse', 'eraser', 'scissors', 'banana',
                'beer', 'cellphone', 'cap', 'coat', 'knife', 'ball', 'dog', 'cat']

class Command(BaseCommand):
    help = 'Changes picture target'

    def handle(self, *args, **options):
        PictureTarget.objects.all().delete()
        newPicture = pictureNames[randint(0, len(pictureNames)-1)]
        PictureTarget.objects.create(name=newPicture)
        