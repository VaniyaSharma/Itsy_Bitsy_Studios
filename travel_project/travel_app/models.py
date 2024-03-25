from django.db import models
from django.contrib.auth.models import User

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    @property
    def duration(self):
        return (self.end_date - self.start_date).days + 1

class Event(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    day_number = models.IntegerField()
    event_title = models.CharField(max_length=200)
    time = models.TimeField()
    description = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)

class Location(models.Model):
    name = models.CharField(max_length=150, null=True)
    description = models.TextField(max_length=2000)

    def __str__(self):
        return self.name