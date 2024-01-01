from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db import models


class UserTypeChoice(models.TextChoices):
    client = "client", "Client"
    business = "business", "Business"


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True

    country = CountryField().formfield()
    phone_number = PhoneNumberField(required=False)
    image = forms.ImageField(required=False)
    goal = forms.ChoiceField(choices=UserTypeChoice.choices)

    class Meta:
        model = User
        fields = ("username", "email",
                  "country", "phone_number",
                  "password1", "password2")


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True

    country = CountryField().formfield()
    phone_number = PhoneNumberField(required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name",
                  "email", "username", "country",
                  "phone_number", "image")
