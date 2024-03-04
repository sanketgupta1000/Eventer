from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Participant)
admin.site.register(Participation)
admin.site.register(FollowList)
admin.site.register(Feedback)