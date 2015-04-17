# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Circuits(models.Model):
    circuitid = models.IntegerField(db_column='circuitId', primary_key=True) # Field name made lowercase.
    circuitref = models.CharField(db_column='circuitRef', max_length=255) # Field name made lowercase.
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    alt = models.IntegerField(blank=True, null=True)
    url = models.CharField(unique=True, max_length=255)
    class Meta:
        managed = False
        db_table = 'circuits'

class Constructorresults(models.Model):
    constructorresultsid = models.IntegerField(db_column='constructorResultsId', primary_key=True) # Field name made lowercase.
    raceid = models.IntegerField(db_column='raceId') # Field name made lowercase.
    constructorid = models.IntegerField(db_column='constructorId') # Field name made lowercase.
    points = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'constructorResults'

class Constructorstandings(models.Model):
    constructorstandingsid = models.IntegerField(db_column='constructorStandingsId', primary_key=True) # Field name made lowercase.
    raceid = models.IntegerField(db_column='raceId') # Field name made lowercase.
    constructorid = models.IntegerField(db_column='constructorId') # Field name made lowercase.
    points = models.FloatField()
    position = models.IntegerField(blank=True, null=True)
    positiontext = models.CharField(db_column='positionText', max_length=255, blank=True) # Field name made lowercase.
    wins = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'constructorStandings'

class Constructors(models.Model):
    constructorid = models.IntegerField(db_column='constructorId', primary_key=True) # Field name made lowercase.
    constructorref = models.CharField(db_column='constructorRef', max_length=255) # Field name made lowercase.
    name = models.CharField(unique=True, max_length=255)
    nationality = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = 'constructors'

class Driverstandings(models.Model):
    driverstandingsid = models.IntegerField(db_column='driverStandingsId', primary_key=True) # Field name made lowercase.
    raceid = models.IntegerField(db_column='raceId') # Field name made lowercase.
    driverid = models.IntegerField(db_column='driverId') # Field name made lowercase.
    points = models.FloatField()
    position = models.IntegerField(blank=True, null=True)
    positiontext = models.CharField(db_column='positionText', max_length=255, blank=True) # Field name made lowercase.
    wins = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'driverStandings'

class Drivers(models.Model):
    driverid = models.IntegerField(db_column='driverId', primary_key=True) # Field name made lowercase.
    driverref = models.CharField(db_column='driverRef', max_length=255) # Field name made lowercase.
    number = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=3, blank=True)
    forename = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    dob = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=255, blank=True)
    url = models.CharField(unique=True, max_length=255)
    class Meta:
        managed = False
        db_table = 'drivers'

class Laptimes(models.Model):
    raceid = models.IntegerField(db_column='raceId') # Field name made lowercase.
    driverid = models.IntegerField(db_column='driverId') # Field name made lowercase.
    lap = models.IntegerField()
    position = models.IntegerField(blank=True, null=True)
    time = models.CharField(max_length=255, blank=True)
    milliseconds = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'lapTimes'

class Pitstops(models.Model):
    raceid = models.IntegerField(db_column='raceId') # Field name made lowercase.
    driverid = models.IntegerField(db_column='driverId') # Field name made lowercase.
    stop = models.IntegerField()
    lap = models.IntegerField()
    time = models.TimeField()
    duration = models.CharField(max_length=255, blank=True)
    milliseconds = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'pitStops'

class Qualifying(models.Model):
    qualifyid = models.IntegerField(db_column='qualifyId', primary_key=True) # Field name made lowercase.
    raceid = models.IntegerField(db_column='raceId') # Field name made lowercase.
    driverid = models.IntegerField(db_column='driverId') # Field name made lowercase.
    constructorid = models.IntegerField(db_column='constructorId') # Field name made lowercase.
    number = models.IntegerField()
    position = models.IntegerField(blank=True, null=True)
    q1 = models.CharField(max_length=255, blank=True)
    q2 = models.CharField(max_length=255, blank=True)
    q3 = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'qualifying'

class Races(models.Model):
    raceid = models.IntegerField(db_column='raceId', primary_key=True) # Field name made lowercase.
    year = models.IntegerField()
    round = models.IntegerField()
    circuitid = models.IntegerField(db_column='circuitId') # Field name made lowercase.
    name = models.CharField(max_length=255)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    url = models.CharField(unique=True, max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'races'

class Results(models.Model):
    resultid = models.IntegerField(db_column='resultId', primary_key=True) # Field name made lowercase.
    raceid = models.IntegerField(db_column='raceId') # Field name made lowercase.
    driverid = models.IntegerField(db_column='driverId') # Field name made lowercase.
    constructorid = models.IntegerField(db_column='constructorId') # Field name made lowercase.
    number = models.IntegerField()
    grid = models.IntegerField()
    position = models.IntegerField(blank=True, null=True)
    positiontext = models.CharField(db_column='positionText', max_length=255) # Field name made lowercase.
    positionorder = models.IntegerField(db_column='positionOrder') # Field name made lowercase.
    points = models.FloatField()
    laps = models.IntegerField()
    time = models.CharField(max_length=255, blank=True)
    milliseconds = models.IntegerField(blank=True, null=True)
    fastestlap = models.IntegerField(db_column='fastestLap', blank=True, null=True) # Field name made lowercase.
    rank = models.IntegerField(blank=True, null=True)
    fastestlaptime = models.CharField(db_column='fastestLapTime', max_length=255, blank=True) # Field name made lowercase.
    fastestlapspeed = models.CharField(db_column='fastestLapSpeed', max_length=255, blank=True) # Field name made lowercase.
    statusid = models.IntegerField(db_column='statusId') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'results'

class Seasons(models.Model):
    year = models.IntegerField(primary_key=True)
    url = models.CharField(unique=True, max_length=255)
    class Meta:
        managed = False
        db_table = 'seasons'

class Status(models.Model):
    statusid = models.IntegerField(db_column='statusId', primary_key=True) # Field name made lowercase.
    status = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = 'status'

