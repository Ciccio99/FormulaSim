from django import forms
from django.forms import extras
from formulaSim.models import *



# Form used to select which race to simulate
class GetRaceForm(forms.Form):
	year = forms.IntegerField(widget=forms.Select(choices=[(i,i) for i in range(2011,2016)], attrs={'class':'race-form-input'}))
	round = forms.IntegerField(widget=forms.Select(choices=[(i,i) for i in range(1,21)], attrs={'class':'race-form-input'}))
	# Take fields directly from Race model for ease
		
