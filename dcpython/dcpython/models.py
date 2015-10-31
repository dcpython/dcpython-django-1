from __future__ import absolute_import
from django.conf import settings
if settings.DEFAULT_FILE_STORAGE == 'cumulus.storage.SwiftclientStorage':
    from cumulus.storage import SwiftclientStorage
    storage = SwiftclientStorage()
else:
    from django.core.files.storage import FileSystemStorage
    storage = FileSystemStorage()
from PIL import Image
from django.db import models
from localflavor.us.models import PhoneNumberField
from django.core.files.base import ContentFile
from datetime import date
from itertools import chain
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils import timezone
from .integration.meetup import get_upcoming_events
from .integration.meetup import get_past_events
import feedparser
from django.conf import settings
try:
    from cStringIO import StringIO
except ImportError:
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO
import base64
import imghdr
import os
import random

# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     meetup_username = models.CharField(max_length=100, blank=True, null=True)
#     meetup_id = models.IntegerField(blank=True, null=True)


class ServiceSync(models.Model):
    """
    keep track of the last time a sync event took place
    """
    service = models.CharField(max_length=200)
    last_synced = models.CharField(max_length=50)


LEVEL_DATA = (("A", "Andrew W. Singer Memorial Level", 2500),
              ("P", "Platinum", 1000), ("G", "Gold", 500),
              ("S", "Silver", 250), ("B", "Bronze", 100),
              ("I", "Individual", 50), ("O", "Other", 0))

DONOR_LEVELS = [(code,
                 "{} (${})".format(name, value), )
                for code, name, value in LEVEL_DATA]

DL_INDEX = {'A': 0, 'P': 1, 'G': 2, 'S': 3, 'B': 4, 'I': 5, 'O': 6, None: 7, }

DONATION_TYPES = (
    #    ("B", "Bank Account"),
    ("C", "Credit Card"),
    #    ("P", "PayPal"),
    ("G", "Pledge"), )


class DonorManager(models.Manager):
    def active(self):
        """ return all active donors - that is donors who have been reviewed
        and have at least one valid, reviwed donation """

        # it is quite possible this query does not actually do what I hope
        # it does.

        return self.filter(reviewed=True).filter(Q(valid_until__gte=date.today(
        )) | Q(donations__valid_until__gte=date.today(),
               donations__reviewed=True))

    def random(self):
        """ return one active donor chosen at random,
        weighted by their level's minimum donation amount """
        donors = self.active()
        bag = []
        for donor in donors:
            bag += donor.get_level()[2] / 50 * [donor]
        return random.choice(bag) if bag else None


class Donor(models.Model):
    """
    Model for Donors to DCPYthon.
    """
    email = models.EmailField()
    phone = PhoneNumberField(blank=True, null=True)
    name = models.CharField(
        max_length=100,
        help_text="If institutional donation, point of contact's name")

    public_name = models.CharField(max_length=100,
                                   verbose_name="Display Name",
                                   blank=True,
                                   null=True)
    public_url = models.URLField(blank=True,
                                 null=True,
                                 verbose_name="Display Url")
    public_slogan = models.CharField(max_length=200,
                                     verbose_name="Display Slogan",
                                     blank=True,
                                     null=True)
    public_logo = models.ImageField(storage=storage,
                                    upload_to="donor_logos",
                                    verbose_name="Display Logo",
                                    blank=True,
                                    null=True)

    help_text = "Override levels specified by donations if not past "
    help_text += "'valid until'"
    level = models.CharField(max_length=1,
                             choices=DONOR_LEVELS,
                             blank=True,
                             null=True,
                             help_text=help_text)
    secret = models.CharField(max_length=90)
    reviewed = models.BooleanField(default=False)
    help_text = "Specify a date until which the level specified for the donor"
    help_text += " is valid. After, donation levels will control."
    valid_until = models.DateField(blank=True, null=True, help_text=help_text)
    objects = DonorManager()

    @property
    def logoIO(self):
        return StringIO(self.public_logo.file.read())

    def save(self, *args, **kwargs):
        # ensure there is a secret
        if not self.secret:
            self.secret = base64.urlsafe_b64encode(os.urandom(64))
        # ensure the image is in a valid format
        if self.public_logo:
            image = self.logoIO
            valid_image = self.process_image(image)
            if valid_image != image:
                self.public_logo.save("{}.png".format(self.pk),
                                      valid_image,
                                      save=False)
        # if self.public_logo:
        #     self.public_logo = self.process_image(self.public_logo.file)
        super(Donor, self).save(*args, **kwargs)

    def process_image(self, f):
        """
        return a file object with the image contained in the f that is:
            a png, gif or jpeg
            no more than 800x450
            no less than 16:9 ratio
        """
        image = Image.open(f)
        width, height = image.size

        if height <= 450 and imghdr.what(f) in [
                'png', 'gif', 'jpeg'
        ] and 1.0 * width / height >= 16.0 / 9:
            return f

        # ensure no more than 450x800
        if height > 450:
            image.thumbnail((450, 800), Image.ANTIALIAS)
            width, height = image.size

        # ensure no more than 16:9 aspect ratio
        if 1.0 * width / height < 16.0 / 9:
            new_width = height * 16 / 9
            new_image = Image.new('RGBA', (new_width, height))
            x = (new_width - width) / 2
            y = 0
            new_image.paste(image, (x, y, x + width, y + height))
            image = new_image

        # generate a png
        string_file = StringIO()
        image.save(string_file, "PNG")
        string_file.seek(0)
        f = ContentFile(string_file.read())
        return f

    def get_level(self):
        """ return the current donor level - it is the donor's level if exists
        and unexpired or the highest active donation level"""
        if self.level and self.valid_until and self.valid_until >= date.today(
        ):
            return LEVEL_DATA[DL_INDEX[self.level]]

        level = DL_INDEX[None]
        for donation in self.donations.filter(reviewed=True,
                                              valid_until__gte=date.today()):
            level = min(level, DL_INDEX[donation.level])

        return LEVEL_DATA[level] if level != DL_INDEX[None] else None

    def pending(self):
        """ return whether the donor or one of their donations is pending
        review """
        return not self.reviewed or self.donations.filter(
            reviewed=False).count()

    def __unicode__(self):
        if self.public_name:
            return u"{} (contact: {}, {})".format(self.public_name, self.name,
                                                  self.email)
        else:
            return u"{} ({})".format(self.name, self.email)


class Donation(models.Model):
    """
    Model representing one donation
    """
    donor = models.ForeignKey(Donor, related_name='donations')
    datetime = models.DateTimeField()
    type = models.CharField(max_length=1, choices=DONATION_TYPES)
    completed = models.BooleanField(default=False)
    donation = models.DecimalField(decimal_places=2, max_digits=10)
    transaction_id = models.CharField(max_length=50)

    valid_until = models.DateField(blank=True, null=True)
    level = models.CharField(max_length=1,
                             choices=DONOR_LEVELS,
                             blank=True,
                             null=True)
    reviewed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.level:
            for lvl in LEVEL_DATA:
                if self.donation >= lvl[2]:
                    self.level = lvl[0]
                    break
        super(Donation, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"${} donation from {} on {}".format(
            self.donation, self.donor.public_name or self.donor.name,
            self.datetime)


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
    phone = models.CharField(max_length=15, default='', blank=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5, blank=True)
    repinned = models.BooleanField()

    @classmethod
    def create_from_meetup(cls, meetup_data):
        meetup_data['meetup_id'] = meetup_data.pop('id')
        meetup_data['zip_code'] = meetup_data.pop('zip', '')
        try:
            venue = cls.objects.get(meetup_id=meetup_data['meetup_id'])
        except cls.DoesNotExist:
            venue = cls(**meetup_data)
        else:
            for k, v in meetup_data.items():
                setattr(venue, k, v)

        venue.full_clean()
        venue.save()
        return venue


class EventManager(models.Manager):
    use_for_related = True

    def upcoming(self):
        i = now()
        return self.filter(Q(start_time__gte=i) | Q(end_time__isnull=False,
                                                    end_time__gte=i))

    def past(self):
        i = now()
        return self.filter(start_time__lt=i).filter(Q(end_time__lt=i) | Q(
            end_time__isnull=True))


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

    @property
    def local_start_time(self):
        current_tz = timezone.get_current_timezone()
        return self.start_time.astimezone(current_tz)

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
        return reverse('event-detail',
                       kwargs={'slug': self.slug,
                               'year': self.local_start_time.year,
                               'month': self.local_start_time.month,
                               'day': self.local_start_time.day})


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
            defaults = {'event': event, 'updated': entry.updated, }
            playlist, created = Playlist.objects.get_or_create(
                remote_id=remote_id,
                defaults=defaults)

            if created:
                continue
            if playlist.updated == entry.updated:
                continue
            playlist.event = event
            playlist.updated = entry.updated
            playlist.save()

        last_synced, created = ServiceSync.objects.get_or_create(
            service=url,
            defaults={'last_synced': feed.feed.updated})
        if not created:
            last_synced.last_synced = feed.feed.updated
            last_synced.save()


class Playlist(models.Model):
    event = models.ForeignKey(Event, related_name='playlists')
    remote_id = models.CharField(max_length=100, blank=True, null=True)
    updated = models.CharField(max_length=30)

    objects = PlaylistManager()
