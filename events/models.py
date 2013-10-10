# encoding: utf-8
from __future__ import absolute_import

from itertools import chain

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils.text import slugify
from django.utils.timezone import now

from app.integration.meetup import get_upcoming_events, get_past_events


class Venue(models.Model):
    meetup_id = models.CharField(unique=True, max_length=32)

    # TODO: switch to GeoDjango PointField?
    lon = models.DecimalField(null=True, max_digits=9, decimal_places=6)
    lat = models.DecimalField(null=True, max_digits=9, decimal_places=6)

    name = models.CharField(max_length=200)
    state = models.CharField(max_length=2)
    address_1 = models.CharField(max_length=200)
    address_2 = models.CharField(max_length=200, blank=True)
    address_3 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5, blank=True)

    repinned = models.BooleanField()

    @classmethod
    def create_from_meetup(cls, meetup_data):
        i, created = cls.objects.get_or_create(meetup_id=meetup_data['id'])

        for k, v in meetup_data.items():
            if k == "id": continue
            setattr(i, k, v)

        i.full_clean()
        i.save()
        return i


class EventManager(models.Manager):
    use_for_related = True

    def upcoming(self):
        i = now()
        return self.filter(Q(start_time__gte=i) | Q(end_time__isnull=False, end_time__gte=i))

    def past(self):
        i = now()
        return self.filter(start_time__lt=i).filter(Q(end_time__lt=i) | Q(end_time__isnull=True))


class Event(models.Model):
    objects = EventManager()

    record_created = models.DateTimeField(auto_now_add=True)
    record_modified = models.DateTimeField(auto_now=True)

    meetup_id = models.CharField(unique=True, max_length=32)

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    venue = models.ForeignKey("Venue", null=True, blank=True)

    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True, blank=True)

    meetup_url = models.URLField(blank=True)

    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('start_time', 'end_time')
        get_latest_by = 'start_time'
        unique_together = (('start_time', 'slug'))

    @classmethod
    def sync_from_meetup(cls):
        for i in chain(get_past_events(), get_upcoming_events()):
            event, created = cls.objects.get_or_create(meetup_id=i['id'])

            for j in ('name', 'description', 'start_time', 'end_time'):
                setattr(event, j, i.get(j))

            event.meetup_url = i['event_url']

            event.slug = slugify(event.name)

            venue = i.get('venue')
            if venue:
                event.venue = Venue.create_from_meetup(venue)

            event.full_clean()
            event.save()

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'slug': self.slug,
                                               'year': self.start_time.year,
                                               'month': self.start_time.month,
                                               'day': self.start_time.day})
