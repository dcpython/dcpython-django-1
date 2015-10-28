from django.core.management.base import BaseCommand, CommandError
from dcpython.events.models import Event


class Command(BaseCommand):
    help = 'Synchronizes the local event database with Meetup.com'

    def handle(self, *args, **options):
        try:
            import bpdb as pdb
        except ImportError:
            import pdb

        try:
            Event.sync_from_meetup()
        except Exception as exc:
            self.stderr.write("ERROR: %s" % exc)
            pdb.pm()