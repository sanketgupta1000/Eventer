from django.db import models
from account.models import Account

# Create your models here.

class Organizer(models.Model):

    account = models.OneToOneField(Account, on_delete=models.CASCADE)

    # name of the company
    name = models.CharField(max_length=100)

    # tagline of the organizer
    tagline = models.CharField(max_length=200)

    # brief description about the organizer
    description = models.TextField()


class OrganizerReport(models.Model):
    
    # which organizer's report
    organizer = models.OneToOneField(Organizer, on_delete=models.CASCADE)

    follow_count = models.IntegerField()

    event_count = models.IntegerField()

    success_rate = models.FloatField()