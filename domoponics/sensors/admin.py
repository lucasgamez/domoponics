from django.contrib import admin

# Register your models here.
from models.models import Sensor, SensorData, Device, DataType

admin.site.register(Sensor)
admin.site.register(SensorData)
admin.site.register(Device)
admin.site.register(DataType)