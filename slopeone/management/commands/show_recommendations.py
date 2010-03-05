from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from slopeone.core import recommend


class Command(BaseCommand):
    help = 'Show predicted ratings for a user_id'
    args = '[userid]'

    def handle(self, *userids, **options):
        for userid in userids:
            try:
                user = User.objects.get(pk=userid)
            except User.DoesNotExist:
                raise CommandError('User with id %s not found' % userid)
            print recommend(user)
