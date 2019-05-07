# from cloudinary.models import CloudinaryField
from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(blank=False, default='1998-08-13')
    license_driver = models.CharField(max_length=13, default='')
    address = models.TextField(default='')
    phone = models.CharField(max_length=10, default='')
    renter = models.BooleanField(default=False)
    tenant = models.BooleanField(default=False)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    # import pillow to work with imagefield
    def __str__(self):
        return f'{self.user.username} Profile'

    # resize the picture to db
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

