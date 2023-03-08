from django.db import models

# Create your models here.

class Sensor(models.Model):
    data_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()

class SensorData(models.Model):
    data = models.FloatField()
    sensor_id = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    