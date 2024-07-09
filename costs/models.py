from django.db import models

class Cost(models.Model):
    def __str__(self):
        return f"{self.trip} - {self.category}"
    
    category = models.CharField(max_length=30)
    amount = models.FloatField()
    trip = models.ForeignKey(
        "trips.Trip",
        related_name="costs",
        on_delete=models.CASCADE)