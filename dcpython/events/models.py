from django.db import models

# Create your models here.

class Venue(models.Model):
    meetup_id = models.IntegerField()
    zip_code = models.CharField(max_length=5)
    lon = models.IntegerField()
    lat = models.IntegerField()
    repinned = models.BooleanField()
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=2)
    address_1 = models.CharField(max_length=200)
    address_2 = models.CharField(max_length=200)
    address_3 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country=models.CharField(max_length=2)


class Event(models.Model):
    meetup_id = models.IntegerField()
    utc_offset = models.IntegerField()
    duration = models.IntegerField()
    time = models.DateTimeField()
    last_updated = models.DateTimeField()
    created = models.DateTimeField()
    meetup_url = models.URLField()
    description = models.TextField()
    name = models.CharField(max_length=200)
    venue = models.ForeignKey("Venue")

    def update_from_meetup_data(self, meetup_data):
        """
        Compare json with existing
        Check against last_updated
        """


class EventManager(models.Manager):
    """
    Custom Event Manager for Event model
    """

    def create_event_from_meetup_data(self, meetup_data):
        """
        Create new event from meetup data
        """
    
    def update_event_from_meetup_data(self, meetup_data):
        """
        Look up ID, get model, and call Model.update_from_meetup_data
        """

    def update_or_create_event_from_meetup_data(self, meetup_data):
        """
        Get ID and see if it exists. If exists call update else create
        """
