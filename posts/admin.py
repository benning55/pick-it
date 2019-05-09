from django.contrib import admin
from .models import Car, Report, Contract
from .models import Image
from .models import Price
from .models import Review, Renting
from django.contrib.auth.models import Permission

# Register your models here.
admin.site.register(Permission)

admin.site.register(Car)

admin.site.register(Image)

admin.site.register(Price)

admin.site.register(Review)

admin.site.register(Renting)


class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'text', 'reported']
    list_per_page = 10


admin.site.register(Report, ReportAdmin)


admin.site.register(Contract)


