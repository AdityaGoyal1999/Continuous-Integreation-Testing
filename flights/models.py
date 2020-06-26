from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.code} - {self.city}"


class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departures')
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrivals')
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.origin} to {self.destination} for {self.duration}."

    # checks the data on creation
    # def clean(self):
    #     if self.origin == self.destination:
    #         raise ValidationError("Origin and destination are the same.")
    #     if self.duration < 0:
    #         raise ValidationError("Duration must be greater than 0.")

    # # overrides the save method
    # def save(self, *args, **kwargs):
    #     self.clean()
        # Calling django's own function
        
        # super().save(*args, **kwargs)
        
    def is_valid(self):
        return (self.origin != self.destination) and (self.duration >= 0)


class Passenger(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.first} {self.last}"