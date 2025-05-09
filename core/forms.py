from django import forms
from .models import Fan

class FanForm(forms.ModelForm):
    class Meta:
        model = Fan
        fields = ['name', 'email', 'phone', 'country', 'membership_tier']
