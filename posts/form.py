from django import forms
import datetime
from django.core.exceptions import ValidationError

from .models import Car, Image, Price, Review, Renting


class CarRegisterForm(forms.ModelForm):
    car_model = forms.CharField(max_length=100)
    detail = forms.Textarea()
    car_license = forms.CharField(max_length=12)
    car_address = forms.CharField(max_length=255, help_text='ที่อยู่ของยานพาหนะที่ต้องการเช่าเพื่อสะดวกในการไปรับรถในโซนพระจอมเกล้า เช่น เกกีงาม2, Vcondo, RNP')

    class Meta:
        model = Car
        exclude = ['owner', 'date_posted']


class ImageCarRegisterForm(forms.ModelForm):
    path = forms.ImageField(label="Image", required=True)

    class Meta:
        model = Image
        exclude = ['car']


class PriceCarRegisterForm(forms.ModelForm):
    hour = forms.IntegerField(label="Price rent per hour", required=True)
    day = forms.IntegerField(label="Price rent per day", required=False)
    week = forms.IntegerField(label="Price rent per week", required=False)
    month = forms.IntegerField(label="Price rent per month", required=False)

    class Meta:
        model = Price
        exclude = ['car']


class ReviewCarForm(forms.ModelForm):
    rating = forms.IntegerField(max_value=5, label="Rate")
    review = forms.CharField(widget=forms.Textarea, label="Description")

    class Meta:
        model = Review
        exclude = ['car']


class RentingCarForm(forms.ModelForm):

    class Meta:
        model = Renting
        exclude = ['user', 'car']
        widgets = {
            'date_time_start': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime'}),
            'date_time_end': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime'}),
            'type_use': forms.Select(),
            'time_use': forms.NumberInput()
        }

    def clean(self):
        date = super().clean()

        start = date.get('date_time_start')
        end = date.get('date_time_end')

        if start > end:
            raise ValidationError('End date cannot come before start sate')
        elif start < datetime.datetime.now().date():
            raise ValidationError('Please do not fill date past')