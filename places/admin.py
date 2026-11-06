from django.contrib import admin

# Register your models here.
from .models import Place, PlaceImage



admin.site.register(Place)
admin.site.register(PlaceImage)