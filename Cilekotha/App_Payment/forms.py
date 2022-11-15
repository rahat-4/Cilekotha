from socket import fromshare
from django import forms

from .models import BillingAddress

class AddressForm(forms.ModelForm):
    template_name = 'App_Payment/billing_address.html'
    class Meta:
        model = BillingAddress
        fields = ['address', 'zipcode', 'city', 'country']

