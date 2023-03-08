from django.shortcuts import render
from sensors.utils import get_sensor_details
# Create your views here.

def sensor_list(request):
    sensors_id = Sensor.objects.values_list('pk', flat=True)
    sensors = []
    for s in sensors_id:
        s = get_sensor_details(s)
    context = {'projects' : sensors}
    return render(request, 'project_index.html', context)