from django.shortcuts import render
from models.models import Sensor, SensorData
import io
from django.http import HttpResponse
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from django.utils.html import format_html

import base64

####################################
## Views for sensors

# List all sensors
def view_sensor_list(request):
    sensors_id = Sensor.objects.values_list('pk', flat=True)
    sensors = []
    for s in sensors_id:
        s = get_sensor_details(s)
        sensors.append(s)
    context = {'sensors' : sensors}
    return render(request, 'sensors/sensor_list.html', context)

# Prompt details of one sensor
# pk (int): primary key of sensor
def view_sensor_detail(request, pk):
    context = {'sensor' : get_sensor_details(pk)}
    return render(request, 'sensors/sensor_detail.html', context)

# Form to add sensor
def view_sensor_add(request):
    render(request, 'sensor/sensor_add.html', {})

########################################
## Utils functions

# Get detail of sensor from database
# sensor_id(int) : primary key of the sensor 
def get_sensor_details(sensor_id):
    sensor = Sensor.objects.get(pk=sensor_id)
    sensor.sensor_data = sensor.sensordata_set.order_by('-timestamp')[:10]
    get_plot_data(sensor)
    return sensor

# Return figure of data from a specific sensor, voir chart js
# sensor(request): return value of a get function for the dataset
def get_plot_data(sensor):
    timestamps = [str(d.timestamp) for d in sensor.sensor_data]
    values = [d.data for d in sensor.sensor_data]

    fig, ax = plt.subplots()
    ax.plot(timestamps, values)
    ax.set_xlabel('Time')
    ax.set_ylabel(sensor.data_type)
    ax.set_facecolor('#eee')
    fig.set_facecolor('#eee')

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_png = buf.getvalue()
    graph = base64.b64encode(image_png)
    sensor.image = graph.decode('utf-8')
    buf.close()

    
