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
	
	errorMessage = ""

	
	if request.method == 'POST':
	# If a POST is placed to select a race to simulate
		
		form = GetRaceForm(data = request.POST)

		# If the form is cleaned out, proceed
		if form.is_valid():

			# Filter through our Race models for a race with the given year and round
			#zeRace = get_or_none(Race, year = form.cleaned_data['year'], round = form.cleaned_data['round'])
			zeRace = get_or_none(Race, raceid = form.cleaned_data['selectRace'].raceid)
			if(zeRace != None):
				

				dictionary.update({'race' : zeRace})
				dictionary.update({'circuit' : Circuit.objects.get(circuitid = zeRace.circuitid)})
				
				# Getting a list of all the final results (One for each driver for that race)
				race_results = Result.objects.filter(raceid = zeRace.raceid).order_by('grid')
				
				dictionary.update({"race_results" : race_results})

				# Getting a list of all drivers
				drivers = []
				for result in race_results:
					drivers.append(Driver.objects.get(driverid=result.driverid))

				dictionary.update({"drivers" : drivers})

				# Serializing the necessary data in json so that javascript can manipulate it
				serialized_drivers = serializers.serialize("json", drivers)
				dictionary.update({'serialized_drivers' : serialized_drivers})
				serialized_laptimes = serializers.serialize("json", Laptime.objects.filter(raceid = zeRace.raceid))
				dictionary.update({'serialized_laptimes' : serialized_laptimes})
				serialized_results = serializers.serialize("json", race_results)
				dictionary.update({'serialized_results' : serialized_results})
				serialized_status = serializers.serialize("json", Status.objects.all())
				dictionary.update({'serialized_status' : serialized_status})
				serialized_pitstops = serializers.serialize("json", Pitstop.objects.filter(raceid = zeRace.raceid))
				dictionary.update({'serialized_pitstops' : serialized_pitstops})

				dictionary.update({'begin_simulation' : True})

				form.selectRace = zeRace;
				dictionary.update({'the_form' : form})
				return render(request, 'formulaSim/raceSim.html', dictionary)
			else:
				errorMessage = "No race exists with the given parameters"
		else:
			errorMessage = "A race must be selected"
	#If request is not a POST
	dictionary.update({'errorMessage' : errorMessage})
	dictionary.update({'begin_simulation' : False})
	dictionary.update({'the_form' : form})
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