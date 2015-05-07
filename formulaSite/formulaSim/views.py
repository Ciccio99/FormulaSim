from django.shortcuts import render, render_to_response 
from django.http import *
from django.template import RequestContext
from django.views import generic
from formulaSim.models import *
from formulaSim.forms import *



def get_or_none(model, *args, **kwargs):
      try:
          return model.objects.get(*args, **kwargs)
      except model.DoesNotExist:
          return None



"""
Three main pages of the web application
Home: home page of what the application is
	|-> About: How we do the database and the simulation,
       	would be very similar to paper
RaceSim: Where the application actually queries the 
          database and shows the simulation
"""
def home(request):
	return render(request, 'formulaSim/home.html')

def raceSim(request):
	dictionary = {}
	form = GetRaceForm()
	dictionary.update({'the_form' : form})
	errorMessage = ""

	
	if request.method == 'POST':
	# If a POST is placed to select a race to simulate
		
		form = GetRaceForm(data = request.POST)

		#If the form is cleaned out, proceed
		if form.is_valid():

			# Filter through our Race models for a race with the given year and round
			zeRace = get_or_none(Race, year = form.cleaned_data['year'], round = form.cleaned_data['round'])
			print "I'm HURRRR"
			if(zeRace != None):

				dictionary.update({'race' : zeRace})

				return render(request, 'formulaSim/raceSim.html', dictionary)
			else:
				errorMessage = "No race exists with the given parameters!"
		
		

	#If request is not a POST
	dictionary.update({'errorMessage' : errorMessage})
	return render(request, 'formulaSim/raceSim.html', dictionary)

"""
Functions for simulation:
"""

"""
Queries database for all Drivers

"""

def drivers(request):
	return render(request, 'formulaSim/getDriverTrial.html', {
		'driver_list': Driver.objects.all()
		})