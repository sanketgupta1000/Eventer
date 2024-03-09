from django import forms
from .models import Event

# form to host an event
class EventHostForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'venue', 'date', 'image', 'category', 'type']