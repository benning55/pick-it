from django.contrib import admin
from .models import Car
from .models import Image
from .models import Price
from .models import Review, Renting

# Register your models here.
admin.site.register(Car)

admin.site.register(Image)

admin.site.register(Price)

admin.site.register(Review)

admin.site.register(Renting)


