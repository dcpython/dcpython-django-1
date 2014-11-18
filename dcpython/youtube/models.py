from django.db import models
from dcpython.app.models import ServiceSync
import feedparser
from dcpython.events.models import Event
from django.conf import settings


class PlaylistManager(models.Manager):
    def sync(self, url=None):
        url = url or settings.YOUTUBE_PLAYLIST_FEED
        feed = feedparser.parse(url)
        try:
            last_synced = ServiceSync.objects.get(service=url)
        except:
            last_synced = None
        else:
            last_synced = last_synced.last_synced

        if feed.feed.updated == last_synced:
            return

        for entry in feed.entries:
            if not entry.summary:
                continue
            try:
                event = Event.objects.get(meetup_url=entry.summary)
            except Event.DoesNotExist:
                continue

            remote_id = entry.id.split('/')[-1]
            defaults = {
                'event': event,
                'updated': entry.updated,
            }
            playlist, created = Playlist.objects.get_or_create(remote_id=remote_id, defaults=defaults)

            if created:
                continue
            if playlist.updated == entry.updated:
                continue
            playlist.event = event
            playlist.updated = entry.updated
            playlist.save()

        last_synced, created = ServiceSync.objects.get_or_create(service=url, defaults={'last_synced': feed.feed.updated})
        if not created:
            last_synced.last_synced = feed.feed.updated
            last_synced.save()

class Playlist(models.Model):
    event = models.ForeignKey(Event, related_name='playlists')
    remote_id = models.CharField(max_length=100, blank=True, null=True)
    updated = models.CharField(max_length=30)

    objects = PlaylistManager()
