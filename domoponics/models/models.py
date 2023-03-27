from django.db import models
from colorfield.fields import ColorField

# Create your models here.

##########################################
# Sensor class is a class that represesnt a physical sensor. The sensor is linked 
# to a data typeand cannot be multi tasking
# dataType: foreign key to a preset DataType
# description: Description of the sensor
# name: name of the sensor
class Sensor(models.Model):
    dataType = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()

##########################################
# SensorData class stores value registered by a sensor. The data-type of the value is retrieved with the sensor
# data: value registered
# sensor_id: foreign_key from the sensor
# timestamp: time of registration (server side)
class SensorData(models.Model):
    data = models.FloatField()
    sensor_id = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    def __str__(self):
        return "{y: '"+ str(self.timestamp.strftime('%Y-%m-%d %H:%M:%S')) +"', X:" + str(self.data) +"}"

##########################################
# Device is the physical object on which sensors are connected, a device can have several sensor
# name: Name of the data type
# location: location of the device on the map
# refresh: Refresh time in minute for sending new registered data
class Device(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    refresh = models.IntegerField()

##########################################
# DataType is a preset type of data (Temperature, humidity ...). Class used for uniformisation of display
# name: Name of the data type
# unit: Unit used in the graph for short display
# color: hexa code for the color to diplay
class DataType(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)
    color = ColorField(format="hexa")