from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# custom account model
class Account(AbstractUser):

    # mobile number of the user
    mobile_no = models.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])

    # type
    class Types(models.TextChoices):
        O = "ORGANIZER", "Organizer"
        P = "PARTICIPANT", "Participant"
    
    type = models.CharField(max_length=30, choices=Types.choices)