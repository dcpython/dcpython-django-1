from django import forms
from dcpython.support.models import Donor, DONATION_TYPES

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        exclude = ["level", "secret", "slogan"]

class DonationForm(forms.Form):
    donation_type = forms.ChoiceField(choices=DONATION_TYPES, widget=forms.HiddenInput)
    cc_token = forms.CharField(max_length=200, widget=forms.HiddenInput, required=False)
    bank_token = forms.CharField(max_length=200, widget=forms.HiddenInput, required=False)
    donation = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0, widget=forms.HiddenInput)

    def clean(self):
        cd = self.cleaned_data
        if cd["donation_type"] == "C" and not cd["cc_token"]:
            raise forms.ValidationError()
        elif cd["donation_type"] == "B" and not cd["bank_token"]:
            raise forms.ValidationError()
        return cd