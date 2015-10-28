from django.core.management.base import BaseCommand, CommandError
from dcpython.youtube.models import Playlist


class Command(BaseCommand):
    help = 'Synchronizes local video playlists with YouTube.com'

    def handle(self, *args, **options):
        Playlist.objects.sync()
