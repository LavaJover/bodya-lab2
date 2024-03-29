from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tour(models.Model):
    country = models.CharField()
    city = models.CharField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    price = models.IntegerField()
class Tourist(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)

class Reservation(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

class Review(models.Model):
    comment = models.CharField()
    rates = models.IntegerField()
    comment_date = models.DateTimeField()
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)