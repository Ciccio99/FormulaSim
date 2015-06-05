from django import forms
from django.forms import extras
from formulaSim.models import *



# Form used to select which race to simulate
class GetRaceForm(forms.Form):
	selectRace = forms.ModelChoiceField(queryset=Race.objects.filter(raceid__gte=840, raceid__lte=931), empty_label='Select a Race',
		widget=forms.Select(attrs={'class':'race-form-input', 'Placeholder' : 'Select a race'}))
	



