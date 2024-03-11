from django.conf import settings
from django.db import models
from organizer.models import Organizer
from account.models import Account

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Event(models.Model):

    # organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    name = models.CharField(max_length = 200)

    description = models.TextField()

    venue = models.CharField(max_length=200)

    date = models.DateTimeField()

    image = models.ImageField(upload_to=settings.MEDIA_ROOT)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    type = models.CharField(max_length=50, choices={("i" , "individual"), ("t" , "team")})

    status = models.CharField(max_length=50, default="u", choices={("u", "upcoming"), ("c", "completed"), ("x", "canceled")})

    class Meta:
        # custom permissions for event
        permissions = [
            ("host_event", "Can host an event"),
            ("delete_own_event", "Can delete own event"),
            ("view_all_event", "Can view all events"),
            ("participate_in_event", "Can participate in event"),
        ]


class EventStats(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    registration_count = models.IntegerField()

    participant_count = models.IntegerField()

    avg_feedback = models.DecimalField(max_digits=2, decimal_places=1)