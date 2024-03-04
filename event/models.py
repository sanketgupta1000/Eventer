from django.db import models
from organizer.models import Organizer

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

class Event(models.Model):

    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)

    name = models.CharField(max_length = 200)

    description = models.TextField()

    venue = models.CharField(max_length=200)

    date = models.DateTimeField()

    image = models.ImageField(upload_to="images/")

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    type = models.CharField(max_length=50, choices={("i" , "individual"), ("t" , "team")})

    status = models.CharField(max_length=50, default="u", choices={("u", "upcoming"), ("c", "completed"), ("x", "canceled")})

class EventStats(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    registration_count = models.IntegerField()

    participant_count = models.IntegerField()

    avg_feedback = models.DecimalField(max_digits=2, decimal_places=1)