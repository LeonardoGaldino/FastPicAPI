from django.core.management.base import BaseCommand, CommandError
from API.models import PictureTarget
from random import randint

pictureNames = ['Pen', 'Notebook', 'Pencil', 'Mouse', 'Eraser', 'Scissors', 'Banana'
                'Beer', 'Cellphone', 'Cap', 'Coat', 'Knife', 'Ball', 'Dog', 'Cat']

class Command(BaseCommand):
    help = 'Changes picture target'

    def handle(self, *args, **options):
        PictureTarget.objects.all().delete()
        newPicture = tests[randint(0, len(pictureNames)-1)]
        PictureTarget.objects.create(name=newPicture)
        