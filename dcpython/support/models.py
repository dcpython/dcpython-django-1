from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField
from PIL import Image
import base64
import os

DONOR_LEVELS = (
    ("P", "Platinum"),
    ("G", "Gold"),
    ("S", "Silver"),
    ("B", "Bronze"),
    ("I", "Individual"),
    ("O", "Other")
)

DONATION_TYPES = (
    ("B", "Bank Account"),
    ("C", "Credit Card"),
    ("P", "PayPal"),
    ("G", "Pledge"),
)

# Create your models here.
class Donor(models.Model):
    """
    Model for Donors to DCPYthon.
    """
    name = models.CharField(max_length=100, verbose_name="Display Name")
    url = models.URLField(blank=True, null=True, verbose_name="Display Url")
    email = models.EmailField()
    phone = PhoneNumberField(blank=True, null=True)
    contact = models.CharField(max_length=300, blank=True, null=True, help_text="name of contact at your organization, if applicable")
    slogan = models.CharField(max_length=200, blank=True, null=True)
    level = models.CharField(max_length=1, choices=DONOR_LEVELS, blank=True, null=True)
    logo = models.ImageField(upload_to="donor_logos", blank=True, null=True)
    secret = models.CharField(max_length=90)

    def save (self, *args, **kwargs):
        if not self.secret:
            self.secret = base64.urlsafe_b64encode(os.urandom(64))
        super(Donor, self).save(*args, **kwargs)

class Donation(models.Model):
    """
    Model representing one donation
    """
    donor = models.ForeignKey(Donor)
    datetime = models.DateTimeField()
    type = models.CharField(max_length=1, choices=DONATION_TYPES)
    completed = models.BooleanField(default=False)
    donation = models.DecimalField(decimal_places=2, max_digits=10)
