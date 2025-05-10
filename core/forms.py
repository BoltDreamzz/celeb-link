from django import forms
from .models import Fan

class FanForm(forms.ModelForm):
    class Meta:
        model = Fan
        fields = ['name', 'email', 'phone', 'country', 'membership_tier']

# forms.py
from django import forms

# forms.py
from django import forms

class MessageForm(forms.Form):
    subject = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'input input-primary w-100',
            'placeholder': 'Subject'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'textarea textarea-primary w-100',
            'placeholder': 'Type your message...',
            'rows': 5
        })
    )
    sender_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'input input-primary w-100',
            'placeholder': 'Your email address'
        })
    )
