from django.db import models
from account.models import Account
from organizer.models import Organizer
from event.models import Event

# Create your models here.

class Participant(models.Model):
    
    account = models.OneToOneField(Account, on_delete=models.CASCADE)


class FollowList(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)

    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)


class Participation(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)

    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    status = models.CharField(max_length=50, default="not_participated")


class Feedback(models.Model):
    # which participant gave feedback
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)

    # to which event gave feedback
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    # what is the rating
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    # what is the feedback
    feedback = models.TextField()