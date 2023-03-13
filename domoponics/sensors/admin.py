from django.contrib import admin

# Register your models here.
from models.models import Sensor, SensorData

admin.site.register(Sensor)
admin.site.register(SensorData)