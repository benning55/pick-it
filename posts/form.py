from django import forms
import datetime
from django.core.exceptions import ValidationError
import logging
import pytz

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
    date_time_start = forms.DateTimeField(help_text="โปรดใส่วันที่ตามรูปแบบนี้ yyyy-mm-dd h:m:s")
    date_time_end = forms.DateTimeField(help_text="โปรดใส่วันที่ตามรูปแบบนี้ yyyy-mm-dd h:m:s")
    license_image = forms.ImageField(label="Image", help_text="ถ่ายรูปคู่บัตรใบขับขี่")

    class Meta:
        model = Renting
        exclude = ['user', 'car']

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('date_time_start')
        end = cleaned_data.get('date_time_end')
        new_start = start.replace(tzinfo=None)
        new_end = end.replace(tzinfo=None)

        if new_start > new_end:
            raise ValidationError('End date cannot come before start sate')
        elif new_start < datetime.datetime.now():
            raise ValidationError('Please do not fill date past')
