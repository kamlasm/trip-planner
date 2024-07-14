from django.contrib.postgres.fields import ArrayField
from django.db import models

class Trip(models.Model):
    def __str__(self):
        return f"{self.name}"
    
    name = models.CharField(max_length=60)
    country = models.CharField(max_length=60)
    start_date = models.DateField()
    end_date = models.DateField()
    flight_out_number = models.CharField(max_length=40, blank=True, default='')
    flight_out_time = models.DateTimeField(null=True, blank=True)
    flight_back_number = models.CharField(max_length=40, blank=True, default='')
    flight_back_time = models.DateTimeField(null=True, blank=True)
    activities = ArrayField(models.CharField(max_length=500, blank=True), default=list)
    itinerary = models.TextField(blank=True, default='')