from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator

class User(AbstractUser):
    email = models.CharField(max_length=50, unique=True, validators=[
            EmailValidator(
                message="Enter a valid email",
                code="invalid_registration",
            ),
        ],)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    trips = models.ManyToManyField(
        "trips.Trip",
        related_name="trips",
        # on_delete=models.CASCADE
    )