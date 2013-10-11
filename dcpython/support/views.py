import json

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from dcpython.support.forms import DonorForm, DonationForm
from dcpython.support.models import Donor
from django.template import RequestContext, loader
from django.conf import settings
import balanced


balanced.configure(settings.BALANCED_SECRET)

# Create your views here.

def support(request):
    context = RequestContext(request)
    context.update({"active": "donate", "donor_form": DonorForm(), "donation_form": DonationForm, "balanced_uri": settings.BALANCED_URI })
    return render(request, 'support/support.html', context)

def donor_update(request, secret=None):
    donor = get_object_or_404(Donor, secret=secret)
    if request.method == 'POST':
        form = DonorForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
    else:
        form = DonorForm(instance=donor)
    context = RequestContext(request)
    context.update({"secret": secret, "form": form, "name": donor.name})
    return render(request, 'support/donor_update.html', context)

def make_donation(request):
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

    if donation_type == "C" or donation_type == "B":
        if donation_type == "C":
            account = balanced.Card.find(donation_data["cc_token"])
        elif donation_type == "B":

            account = balanced.BankAccount.find(donation_data["bank_token"])
            account.verify()

        resp = account.debit(amount=donation_amount, appears_on_statement_as="DCPython.org" )

        return HttpResponse(json.dumps(resp))

