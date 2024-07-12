from django.db import models

class Hotel(models.Model):
    def __str__(self):
        return f"{self.trip} - {self.name}"
    
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=500, blank=True, null=True)
    trip = models.ForeignKey(
        "trips.Trip",
        related_name="hotels",
        on_delete=models.CASCADE)