#from django.db import models
#from django.contrib.auth.models import AbstractUser
#
#class User(AbstractUser):
#    meetup_username = models.CharField(max_length=100, blank=True, null=True)
#    meetup_id = models.IntegerField(blank=True, null=True)
#
#class ServiceSync(models.Model):
#    """
#    keep track of the last time a sync event took place
#    """
#    service = models.CharField(max_length=200)
#    last_synced = models.CharField(max_length=50)
