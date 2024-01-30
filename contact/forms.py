from django import forms
from crispy_forms.helper import FormHelper
from phonenumber_field.formfields import PhoneNumberField
from .models import Contact


class ContactForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['name'].widget.attrs['placeholder'] = 'Your Name'
        self.fields['phone'].widget.attrs['placeholder'] = '+353123456789'
        self.fields['email'].widget.attrs['placeholder'] = 'Your Email'
        self.fields['message'].widget.attrs['placeholder'] = 'Your Message'

    phone = PhoneNumberField(widget=forms.TextInput(
        attrs={'placeholder': ('+353123456789')}))

    class Meta:
        model = Contact
        fields = (
            'name',
            'phone',
            'email',
            'message')