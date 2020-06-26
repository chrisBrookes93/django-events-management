from django import forms
from .models import Event


class EventCreationForm(forms.Form):

    class Meta(forms.Form):
        model = Event
        fields = ['title', 'description', 'date_time', 'date_time']


