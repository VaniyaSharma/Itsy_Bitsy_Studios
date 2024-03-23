from django.db import models

class Day(models.Model):
    date = models.DateField()

class Event(models.Model):
    title = models.CharField(max_length=100)
    time = models.TimeField()
    description = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return self.title
