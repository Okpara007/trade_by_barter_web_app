from django import forms
from .models import Listing
from .models import TradeRequest

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'category', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image and image.size > 10*1024*1024:  # 10 MB
            raise forms.ValidationError("Image file too large ( > 10mb )")
        return image

class TradeRequestForm(forms.ModelForm):
    class Meta:
        model = TradeRequest
        fields = ['message']

class ListingSearchForm(forms.Form):
    # category = forms.CharField(required=False, label="Category")
    # location = forms.CharField(required=False, label="Location")
    # trade_preferences = forms.CharField(required=False, label="Trade Preferences")
    query = forms.CharField(required=False, label="Search")