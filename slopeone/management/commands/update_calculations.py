from django.core.management.base import NoArgsCommand
from slopeone.core import update


class Command(NoArgsCommand):
    help = 'Update Calculation table for django-slopeone.'

    def handle(self, *app_labels, **options):
        update()
