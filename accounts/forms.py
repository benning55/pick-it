from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    YEARS = [x for x in range(1940, 2021)]

    email = forms.EmailField(help_text='required')
    first_name = forms.CharField(label='FirstName', max_length=100)
    last_name = forms.CharField(label='LastName', max_length=100)
    dob = forms.DateField(label='DateOfBirth', widget=forms.SelectDateWidget(years=YEARS))
    license_driver = forms.CharField(label='LicenseDriver')
    address = forms.CharField(label='Address', max_length=500, widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'dob', 'license_driver', 'address']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
