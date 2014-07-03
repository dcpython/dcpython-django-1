# import balanced
import stripe
import json

from django.core.mail import send_mail, mail_admins
from dcpython.support.forms import DonorForm, PublicDonorForm, DonationForm
from dcpython.support.models import Donor, Donation
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext, loader
import datetime
stripe.api_key = settings.STRIPE_PRIVATE

def support(request):
    # get all donors that are not pending and that have a valid donation
    all_donors = Donor.objects.active()

    # create a dict of all active donors, sorted into their respective levels
    levels = {}
    for donor in all_donors:
        donors = levels.setdefault(donor.get_level()[1], [])
        donors.append(donor)

    context = RequestContext(request)
    context.update({"donor_form": DonorForm(), "donation_form": DonationForm, "stripe_public": settings.STRIPE_PUBLIC, "levels": levels })
    return render(request, 'support/support.html', context)

def donor_update(request, secret=None):
    donor = get_object_or_404(Donor, secret=secret)
    if request.method == 'POST':
        form = DonorForm(request.POST, instance=donor)
        public_form = PublicDonorForm(request.POST, request.FILES, instance=donor)
        if form.is_valid() and public_form.is_valid():
            donor = form.save()
            # public_form = PublicDonorForm(request.POST, request.FILES, instance=donor)
            donor = public_form.save()
    else:
        form = DonorForm(instance=donor)
        public_form = PublicDonorForm(instance=donor)
    context = RequestContext(request)
    context.update({"secret": secret, "form": form, "public_form": public_form, "name": donor.name, 'donor': donor})
    return render(request, 'support/donor_update.html', context)

def make_donation(request):
    """
    this method is called via ajax by the donate page. 
    if form is invalid, returns form containing error messages else,
    makes debit and redirects.
    """
    if request.method != 'POST':
        return HttpResponse(json.dumps({"error": "only POST supported"}))

    donor_form = DonorForm(request.POST)
    donation_form = DonationForm(request.POST)

    if not donor_form.is_valid():
        context = RequestContext(request)
        context.update({"donor_form": donor_form, "donation_form": donation_form})
        template = loader.get_template('support/donate_ajax.html')
        return HttpResponse(json.dumps({"html": template.render(context)}))

    if not donation_form.is_valid():
        return HttpResponse(json.dumps({"error": "Server Error; please reload and try again."}))

    donation_data = donation_form.cleaned_data
    donation_type = donation_data["donation_type"]
    donation_amount = donation_data["donation"]
    
    donor_data = donor_form.cleaned_data

    if donation_type == "C":

        # Create the charge on Stripe's servers - this will charge the user's card
        try:
          resp = stripe.Charge.create(
              amount=donation_amount*100, # amount in cents, again
              currency="usd",
              card=donation_data['cc_token'],
              description=donor_data['email']
          )
        except stripe.CardError as e:
            resp = {"payment_error": str(e)}
            return HttpResponse(json.dumps(resp))

        # we have a completed charge. save donor and donation to db.
        donor = donor_form.save()
        donation = Donation(donor=donor, datetime=datetime.datetime.fromtimestamp(resp.created), type='C', completed=True, donation=resp.amount/100.0, transaction_id=resp.id)
        donation.save()

    if donation_type == "G":
        # we have a pending donation. save donor and donation to db.
        donor = donor_form.save()
        donation = Donation(donor=donor, datetime=datetime.datetime.utcnow(), type='G', completed=False, donation=donation_amount)
        donation.save()

    body = \
"""
Dear {},

Thank you for your generous {} of ${} DCPython.

You can update your profile at any time by accessing the following link:

http://dcpython.org/donor/{}

{}

Best,

Alex Clark
President, DCPython
"""
    donation = 'We will process your donation shortly. It may take several days before it is reflected on the website.'
    pledge = 'We will contact you shortly regarding your pledge.'
    body = body.format(
        donor.name,
        'pledge' if donation_type == 'G' else 'donation',
        donation_amount,
        donor.secret,
        pledge if donation_type == 'G' else donation
        )

    send_mail('Thank you for your support.', body, 'no-reply@dcpython.org',
        [donor.email], fail_silently=False)

    mail_admins('Donation pending', 'Donation pending', fail_silently=False, connection=None, html_message=None)
    resp = {'redirect': '/donor/{}'.format(donor.secret)}
    return HttpResponse(json.dumps(resp))