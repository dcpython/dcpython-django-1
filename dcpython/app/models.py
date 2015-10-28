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
from django.db.models import Q
import feedparser
from dcpython.events.models import Event
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
