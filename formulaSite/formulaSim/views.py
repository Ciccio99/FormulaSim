from django.shortcuts import render
from django.http import *

from model import *

# Create your views here.

"""
Three main pages of the web application
Home: home page of what the application is
About: How we do the database and the simulation,
       would be very similar to paper
RaceSim: Where the application actually queries the 
          database and shows the simulation
"""
def home(request):
	return render(request, 'home.html')

def about(request):
	return render(request, 'about.html')

def raceSim(request):
	return render(request, 'raceSim.html')

"""
Functions for simulation:
"""

"""
Queries database for all Drivers

"""
def showAllDrivers(request):
	return render(request, 'getDriverTrial.html', {
		'driver_list': Drivers.objects.all()
		}