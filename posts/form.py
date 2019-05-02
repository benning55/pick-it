from django import forms
from .models import Car, Image, Price, Review


class CarRegisterForm(forms.ModelForm):
    car_model = forms.CharField(max_length=100)
    detail = forms.Textarea()
    car_license = forms.CharField(max_length=12)

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
