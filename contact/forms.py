from django import forms
from crispy_forms.helper import FormHelper
from .models import Contact


class ContactForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['name'].widget.attrs['placeholder'] = 'Your Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Your Email'
        self.fields['message'].widget.attrs['placeholder'] = 'Your Message'


    class Meta:
        model = Contact
        fields = (
            'name',
            'email',
            'message')