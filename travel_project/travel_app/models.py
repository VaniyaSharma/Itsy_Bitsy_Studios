from django.db import models
from django.contrib.auth.models import User

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()

class Itinerary(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    day_number = models.IntegerField()
    events = models.ManyToManyField('Event')

class Event(models.Model):
    title = models.CharField(max_length=100)
    time = models.TimeField()
    description = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
