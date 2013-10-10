# encoding: utf-8
from __future__ import absolute_import

from warnings import warn

from apiclient.discovery import build

from django.core.cache import cache
from django.conf import settings

API_KEY = settings.GOOGLE_API_KEY
CHANNEL_ID = settings.YOUTUBE_CHANNEL_ID

if not API_KEY or not CHANNEL_ID:
    warn("Configure the GOOGLE_API_KEY and YOUTUBE_CHANNEL_ID settings for Youtube support")

YOUTUBE = build('youtube', 'v3', developerKey=API_KEY)


def get_playlists():
    playlists = cache.get("youtube_playlists_%s" % CHANNEL_ID)
    if playlists is None:
        playlists = YOUTUBE.playlists().list(part='id,snippet', channelId=CHANNEL_ID).execute()["items"]
        cache.set("youtube_playlists_%s" % CHANNEL_ID, playlists, 60)

    for playlist in playlists:
        yield playlist['id'], playlist['snippet']['title']


def get_playlist_items(playlist_id):
    items_request = YOUTUBE.playlistItems().list(playlistId=playlist_id,
                                                 part="snippet",
                                                 maxResults=50)

    while items_request:
        response = items_request.execute()

        for item in response['items']:
            title = item['snippet']['title']
            video_id = item['snippet']['resourceId']['videoId']
            yield video_id, title

        items_request = YOUTUBE.playlistItems().list_next(items_request, response)


def find_playlist(name, date):
    # We'll look for both zero padding and unpadded dates:
    date_keys = (date.strftime("%Y-%m-%d"), "%s-%s-%s" % (date.year, date.month, date.day))

    for id, title in get_playlists():
        if name == title or any(i in title for i in date_keys):
            return id
