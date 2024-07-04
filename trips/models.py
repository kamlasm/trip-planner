from django.contrib.postgres.fields import ArrayField
from django.db import models

class Trip(models.Model):
    def __str__(self):
        return f"{self.country}"
    
    country = models.CharField(max_length=60)
    cities = ArrayField(models.CharField(max_length=60))
    start_date = models.DateField()
    end_date = models.DateField()
    hotels = ArrayField(models.CharField(max_length=200))
    flight_out_number = models.CharField(max_length=10)
    flight_out_time = models.DateTimeField()
    flight_back_number = models.CharField(max_length=10)
    flight_back_time = models.DateTimeField()
    activities = ArrayField(models.CharField(max_length=200), blank=True)
    itinerary = models.TextField()
    budget = models.FloatField()
    hotels_cost = models.FloatField()
    flights_cost = models.FloatField()     