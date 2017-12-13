from django.core.management.base import BaseCommand, CommandError
from API.models import PictureTarget
from random import randint

pictureNames = ['pen', 'notebook', 'pencil', 'mouse', 'eraser', 'scissors', 'banana',
                'beer', 'cellphone', 'cap', 'coat', 'knife', 'ball', 'dog', 'cat']

class Command(BaseCommand):
    help = 'Changes picture target'

    def handle(self, *args, **options):
        current_picture = PictureTarget.objects.all()[0]
        current_name = current_picture.name
        current_picture.delete()
        newPicture = pictureNames[randint(0, len(pictureNames)-1)]
        while newPicture == current_name:
            newPicture = pictureNames[randint(0, len(pictureNames)-1)]
        PictureTarget.objects.create(name=newPicture)
        