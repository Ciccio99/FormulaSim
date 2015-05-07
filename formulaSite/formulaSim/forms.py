from django import forms
from django.forms import extras
from formulaSim.models import *



# Form used to select which race to simulate
class GetRaceForm(forms.ModelForm):

	# Take fields directly from Race model for ease
	class Meta:
		model = Race

		fields = ('year', 'round')

		widgets = {
            'year' : forms.NumberInput(attrs = {'Placeholder' : 'Season Year'}),
            'round' : forms.NumberInput(attrs = {'Placeholder' : 'Race Round'}),
            }

