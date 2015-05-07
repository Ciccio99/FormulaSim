from django.shortcuts import render
from django.http import *

from formulaSim.models import *

# Create your views here.

"""
Three main pages of the web application
Home: home page of what the application is
	|-> About: How we do the database and the simulation,
       	would be very similar to paper
RaceSim: Where the application actually queries the 
          database and shows the simulation
"""
def home(request):
	return render(request, 'home.html')

def raceSim(request):
	return render(request, 'raceSim.html')

"""
Functions for simulation:
"""

"""
Queries database for all Drivers

"""

def drivers(request):
	return render(request, 'getDriverTrial.html', {
		'driver_list': Driver.objects.all()
		})