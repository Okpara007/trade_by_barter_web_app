# marketplace/forms.py

from django import forms
from .models import Listing
from .models import TradeRequest

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'image']

class TradeRequestForm(forms.ModelForm):
    class Meta:
        model = TradeRequest
        fields = ['message']