from django import forms
from .models import Service

class OrderForm(forms.Form):
    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        widget=forms.Select(attrs={
            'class': 'w-full p-2 border rounded-lg border-gray-300 focus:ring focus:outline-none'
        })
    )
    link = forms.URLField(
        widget=forms.URLInput(attrs={
            'placeholder': 'https://example.com/UserName',
            'class': 'w-full p-2 border rounded-lg border-gray-300 focus:ring focus:outline-none'
        })
    )
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter quantity',
            'class': 'w-full p-2 border rounded-lg border-gray-300 focus:ring focus:outline-none'
        })
    )