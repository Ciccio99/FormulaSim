from django.db import models

# Create your models here.
"""
Models based on ER-Diagram

No ids added since Django adds them,
Changed id references to ForeignKeys

Change however
"""


"""
Model of Driver
"""
class Driver(models.Model):
	number = models.IntegerField(default = 0)
	code = models.CharField(max_length=50)
	forename = models.CharField(max_length=50)
	surname = models.CharField(max_length=50)
	dob = models.CharField(max_length=20)
	nationality = models.CharField(max_length=50)

	def __str__(self):
		return self.name

"""
Model of Results
"""
class Results(models.Model):
	raceID = models.ForeignKey('Race')
	driverID = models.ForeignKey('Driver')
	constructorID = models.ForeignKey('Constructors')
	number = models.IntegerField()
	grid = models.IntegerField()
	position = models.IntegerField()
	positionText = models.CharField(max_length=50)
	positionOrder = models.IntegerField()
	points = models.DecimalField(max_digits=20, decimal_places=10)
	laps = models.IntegerField()
	time = models.CharField(max_length=50)
	milliseconds = models.IntegerField()
	fastestLap = models.IntegerField()
	rank = models.IntegerField()
	fastestLapTime = models.CharField(max_length=50)
	statusID = models.IntegerField()

	def __str__(self):
		return self.position

"""
Model of Constructors
"""
class Constructors(models.Model):
	name = models.CharField(max_length=50)
	nationality = models.CharField(max_length=50)

	def __str__(self):
		return self.name

"""
Model of Qualifying
"""
class Qualifying(models.Model):
	raceID = models.ForeignKey('Race')
	driverID = models.ForeignKey('Driver')
	constructorID = models.ForeignKey('Constructors')
	number = models.IntegerField()
	position = models.IntegerField()
	q1 = models.CharField(max_length=50)
	q2 = models.CharField(max_length=50)
	q3 = models.CharField(max_length=50)

	def __str__(self):
		return self.q1

"""
Model of PitStops
"""
class PitStops(models.Model):
	lap = models.IntegerField()
	driverID = models.ForeignKey('Driver')
	raceID = models.ForeignKey('Race')
	stop = models.IntegerField()
	time = models.IntegerField()
	duration = models.CharField(max_length=50)
	milliseconds = models.IntegerField()

	def __str__(self):
		return self.duration

"""
Model of LapTimes
"""
class LapTimes(models.Model):
	raceID = models.ForeignKey('Race')
	driverID = models.ForeignKey('Driver')
	lap = models.IntegerField()
	position = models.IntegerField()
	time = models.CharField(max_length=20)
	milliseconds = models.IntegerField()

	def __str__(self):
		return self.time

"""
Model of DriverStandings
"""
class DriverStandings(models.Model):
	raceID = models.ForeignKey('Race')
	driverID = models.ForeignKey('Driver')
	points = models.DecimalField(max_digits=20, decimal_places=10)
	position = models.IntegerField()
	positionText = models.CharField(max_length=50)
	wins = models.IntegerField()

	def __str__(self):
		return self.points

"""
Model of Seasons
"""
class Seasons(models.Model):
	year = models.IntegerField()

	def __str__(self):
		return self.year

"""
Model of Circuit
"""
class Circuit(models.Model):
	name = models.CharField(max_length=50)
	location = models.CharField(max_length=50)
	country = models.CharField(max_length=50)
	latitude = models.DecimalField(max_digits=20, decimal_places=10)
	longitude = models.DecimalField(max_digits=20, decimal_places=10)
	altitude = models.DecimalField(max_digits=20. decimal_places=10)

	def __str__(self):
		return self.name

"""
Model of Race
"""
class Race(models.Model):
	year = models.IntegerField()
	round = models.IntegerField()
	circuitID = models.ForeignKey('Circuit')
	name = models.CharField(max_length=50)
	date = models.CharField(max_length=50)
	time = models.CharField(max_length=50)
	season = models.ForeignKey('Seasons')

	def __str__(self):
		return self.name