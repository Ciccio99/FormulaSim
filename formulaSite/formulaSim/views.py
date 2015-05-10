from django.shortcuts import render, render_to_response 
from django.http import *
from django.template import RequestContext
from django.views import generic
from formulaSim.models import *
from formulaSim.forms import *
from django.core import serializers
import pdb; 


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

		# If the form is cleaned out, proceed
		if form.is_valid():

			# Filter through our Race models for a race with the given year and round
			zeRace = get_or_none(Race, year = form.cleaned_data['year'], round = form.cleaned_data['round'])
			if(zeRace != None):
				# Load JSON serializer
				json_serializer = serializers.get_serializer("json")()

				dictionary.update({'race' : zeRace})
				
				# Getting a list of all the final results (One for each driver for that race)
				race_results = Result.objects.filter(raceid = zeRace.raceid)
				dictionary.update({"race_results" : race_results})

				# Getting a list of all driver IDs so that they can be used for filtering purposes
				drivers_id  = []
				for result in race_results:
					drivers_id.append(result.driverid) 
				# Getting all drivers based on the driver IDs in the race
				drivers = Driver.objects.filter(driverid__in = drivers_id)
				dictionary.update({"drivers" : drivers})


				serialized_drivers = serializers.serialize("json", drivers)
				dictionary.update({'serialized_drivers' : serialized_drivers})
				serialized_laptimes = serializers.serialize("json", Laptime.objects.filter(raceid = zeRace.raceid))
				dictionary.update({'serialized_laptimes' : serialized_laptimes})
				serialized_results = serializers.serialize("json", race_results)
				dictionary.update({'serialized_results' : serialized_results})
				serialized_status = serializers.serialize("json", Status.objects.all())
				dictionary.update({'serialized_status' : serialized_status})

				return render(request, 'formulaSim/raceSim.html', dictionary)
			else:
				errorMessage = "No race exists with the given parameters!"
		else:
			errorMessage = "All Fields Must be filled out!"
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