from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(help_text='required')
    first_name = forms.CharField(label='FirstName', max_length=100)
    last_name = forms.CharField(label='LastName', max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='FirstName', max_length=100)
    last_name = forms.CharField(label='LastName', max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    YEARS = [x for x in range(1940, 2021)]
    dob = forms.DateField(label='DateOfBirth', widget=forms.SelectDateWidget(years=YEARS))
    license_driver = forms.CharField(label='LicenseDriver')
    address = forms.CharField(label='Address', max_length=500, widget=forms.Textarea)
    phone = forms.CharField(max_length=10)

    class Meta:
        model = Profile
        fields = ['image', 'dob', 'license_driver', 'address', 'phone']
