from django.core.management.base import BaseCommand, CommandError
from dcpython.events.models import Event


class Command(BaseCommand):
    help = 'Synchronizes the local event database with Meetup.com'

    def handle(self, *args, **options):

        Event.sync_from_meetup()
