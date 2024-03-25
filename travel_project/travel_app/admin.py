from django.contrib import admin
from .models import Trip, Event, Location

# Register your models here.
admin.site.register(Trip)
admin.site.register(Event)
admin.site.register(Location)