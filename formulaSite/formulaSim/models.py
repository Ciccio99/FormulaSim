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

class Circuit(models.Model):
    circuitid = models.IntegerField(db_column='circuitId', primary_key=True) # Field name made lowercase.
    circuitref = models.CharField(db_column='circuitRef', max_length=255) # Field name made lowercase.
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    alt = models.IntegerField(blank=True, null=True)
    url = models.CharField(unique=True, max_length=255)

    def __unicode__(self):
        return self.name;
    class Meta:
        managed = True
        db_table = 'circuits'
        verbose_name_plural = 'Circuits'

class ConstructorResult(models.Model):
    constructorresultsid = models.IntegerField(db_column='constructorResultsId', primary_key=True) # Field name made lowercase.
    raceid = models.IntegerField(db_column='raceId') # Field name made lowercase.
    constructorid = models.IntegerField(db_column='constructorId') # Field name made lowercase.
    points = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True)
    
    def __unicode__(self):
        return 'Constructor ID: ' + str(self.constructorresultsid);

    class Meta:
        managed = True
        db_table = 'constructorResults'

class ConstructorStanding(models.Model):
    constructorstandingsid = models.IntegerField(db_column='constructorStandingsId', primary_key=True) # Field name made lowercase.
    raceid = models.IntegerField(db_column='raceId') # Field name made lowercase.
    constructorid = models.IntegerField(db_column='constructorId') # Field name made lowercase.
    points = models.FloatField()
    position = models.IntegerField(blank=True, null=True)
    positiontext = models.CharField(db_column='positionText', max_length=255, blank=True) # Field name made lowercase.
    wins = models.IntegerField()
    
    def __unicode__(self):
        return 'Constructor Standings ID: ' + str(self.constructorstandingsid);

    class Meta:
        managed = True
        db_table = 'constructorStandings'

class Constructor(models.Model):
    constructorid = models.IntegerField(db_column='constructorId', primary_key=True) # Field name made lowercase.
    constructorref = models.CharField(db_column='constructorRef', max_length=255) # Field name made lowercase.
    name = models.CharField(unique=True, max_length=255)
    nationality = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.constructorref;

    class Meta:
        managed = True
        db_table = 'constructors'

class DriverStanding(models.Model):
    driverstandingsid = models.IntegerField(db_column='driverStandingsId', primary_key=True) # Field name made lowercase.
    raceid = models.IntegerField(db_column='raceId') # Field name made lowercase.
    driverid = models.IntegerField(db_column='driverId') # Field name made lowercase.
    points = models.FloatField()
    position = models.IntegerField(blank=True, null=True)
    positiontext = models.CharField(db_column='positionText', max_length=255, blank=True) # Field name made lowercase.
    wins = models.IntegerField()
    
    def __unicode__(self):
        return 'Drivers Standings ID: ' + str(self.driverstandingsid);

    class Meta:
        managed = True
        db_table = 'driverStandings'

class Driver(models.Model):
    driverid = models.IntegerField(db_column='driverId', primary_key=True) # Field name made lowercase.
    driverref = models.CharField(db_column='driverRef', max_length=255) # Field name made lowercase.
    number = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=3, blank=True)
    forename = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    dob = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=255, blank=True)
    url = models.CharField(unique=True, max_length=255)
    
    def __unicode__(self):
        return self.forename + " " + self.surname;

    class Meta:
        managed = True
        db_table = 'drivers'

class Laptime(models.Model):
    laptimeid = models.IntegerField(db_column='laptimeId', primary_key=True) # Field name made lowercase.
    raceid = models.IntegerField(db_column='raceId') # Field name made lowercase.
    driverid = models.IntegerField(db_column='driverId') # Field name made lowercase.
    lap = models.IntegerField()
    position = models.IntegerField(blank=True, null=True)
    time = models.CharField(max_length=255, blank=True)
    milliseconds = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return 'Laptime Race ID: ' + str(self.raceid);

    class Meta:
        ordering = ['lap']
        managed = True
        db_table = 'lapTimes'

class Pitstop(models.Model):
    pitstopid = models.IntegerField(db_column='pitstopId', primary_key=True) # Field name made lowercase.
    raceid = models.IntegerField(db_column='raceId') # Field name made lowercase.
    driverid = models.IntegerField(db_column='driverId') # Field name made lowercase.
    stop = models.IntegerField()
    lap = models.IntegerField()
    time = models.TimeField()
    duration = models.CharField(max_length=255, blank=True)
    milliseconds = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return 'PitStop Race ID: ' + str(self.raceid);

    class Meta:
        managed = True
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
    
    def __unicode__(self):
        return 'Qualifying ID: ' + str(self.qualifyid);

    class Meta:
        managed = True
        db_table = 'qualifying'

class Race(models.Model):
    raceid = models.IntegerField(db_column='raceId', primary_key=True) # Field name made lowercase.
    year = models.IntegerField()
    round = models.IntegerField()
    circuitid = models.IntegerField(db_column='circuitId') # Field name made lowercase.
    name = models.CharField(max_length=255)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    url = models.CharField(unique=True, max_length=255, blank=True)
    
    def __unicode__(self):
        return 'Race ID: ' + str(self.raceid);

    class Meta:
        managed = True
        db_table = 'races'

class Result(models.Model):
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
    
    def __unicode__(self):
        return "Result for Race ID: " + str(self.raceid);

    class Meta:
        managed = True
        db_table = 'results'


class Season(models.Model):
    year = models.IntegerField(primary_key=True)
    url = models.CharField(unique=True, max_length=255)
    
    def __unicode__(self):
        return 'Race Year: ' + str(self.year);

    class Meta:
        managed = True
        db_table = 'seasons'

class Status(models.Model):
    statusid = models.IntegerField(db_column='statusId', primary_key=True) # Field name made lowercase.
    status_name = models.CharField(db_column='status',max_length=255)
    
    def __unicode__(self):
        return self.status_name;

    class Meta:
        managed = True
        db_table = 'status'
        verbose_name_plural = 'Statuses'

