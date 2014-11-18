# encoding: utf-8
from __future__ import absolute_import

from functools import wraps
import datetime

from dateutil.tz import tzutc
from django.conf import settings
from universalclient import Client

# Meetup API
MEETUP = Client("http://api.meetup.com").setArgs(params={"key": settings.MEETUP_API_KEY})

# Upcoming events
UPCOMING_EVENTS = MEETUP._('2').events.setArgs(params={"group_urlname": "dcpython"})

# Past events
PAST_EVENTS = MEETUP._('2').events.setArgs(params={"group_urlname": "dcpython", "status": "past"})


# Via https://github.com/pythonkc/pythonkc-meetups/blob/master/pythonkc_meetups/parsers.py#L102
def parse_datetime_ms(utc_timestamp_ms, utc_offset_ms=None):
    """
    Create a timezone-aware ``datetime.datetime`` from the given UTC timestamp
    (in milliseconds), if provided. If an offest it given, it is applied to the
    datetime returned.

    Parameters
    ----------
    utc_timestamp_ms
        UTC timestamp in milliseconds.
    utc_offset_ms
        Offset from UTC, in milliseconds, to apply to the time.

    Returns
    -------
    A ``datetime.datetime`` if a timestamp is given, otherwise ``None``.
    """

    utc_timestamp_s = utc_timestamp_ms / 1000

    dt = datetime.datetime.fromtimestamp(utc_timestamp_s, tzutc())

    if utc_offset_ms:
        utc_offset_s = utc_offset_ms / 1000
        dt + datetime.timedelta(seconds=utc_offset_s)

    return dt


def normalize_timestamps(f):
    """Ensure that the returned event dictionaries have start_time / end_time datetime instances"""
    @wraps(f)
    def inner(*args, **kwargs):
        for i in f(*args, **kwargs):
            i['start_time'] = parse_datetime_ms(i['time'], i['utc_offset'])
            if 'duration' in i:
                i['end_time'] = i['start_time'] + datetime.timedelta(milliseconds=i['duration'])
            yield i

    return inner


@normalize_timestamps
def get_upcoming_events(count=None):
    res = UPCOMING_EVENTS.get().json().get('results')
    if count is not None:  # TODO: Optimize the API call to avoid querying more than we need
        res = res[:count]
    return res


@normalize_timestamps
def get_past_events(count=None):
    res = PAST_EVENTS.get().json().get('results')
    if count is not None:  # TODO: Optimize the API call to avoid querying more than we need
        res = res[:count]
    return res
