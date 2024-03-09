from django import forms
from .models import Organizer

class OrganizerCreationForm(forms.ModelForm):
    class Meta:
        model = Organizer
        fields = ['name', 'tagline', 'description']