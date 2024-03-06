from django import forms
from .models import Participant

class ParticipantCreationForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = []