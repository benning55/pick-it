from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    car_model = models.CharField(max_length=100)
    detail = models.TextField()
    car_license = models.CharField(max_length=255)
    date_posted = models.DateTimeField(default=timezone.now)
    car_address = models.CharField(max_length=100, default='None')

    def __str__(self):
        return f'{self.owner.username} Car {self.car_model}'


class Image(models.Model):
    path = models.ImageField(default='default1.jpg', upload_to='cars_pics')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.car.owner.username} Car Image {self.car.car_model}'


class Review(models.Model):
    rating = models.IntegerField(default=0)
    review = models.TextField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.car.owner.username} review {self.car.car_model} '


class Price(models.Model):
    hour = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    week = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.car.owner.username} Price {self.car.car_model}'
