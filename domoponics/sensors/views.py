from django.shortcuts import render
from models.models import Sensor, SensorData
import io
from django.http import HttpResponse
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from django.utils.html import format_html

import base64

def sensor_list(request):
    sensors_id = Sensor.objects.values_list('pk', flat=True)
    sensors = []
    for s in sensors_id:
        s = get_sensor_details(s)
        sensors.append(s)
    context = {'sensors' : sensors}
    return render(request, 'sensors/sensor_list.html', context)


def get_sensor_details(sensor_id):
    sensor = Sensor.objects.get(pk=sensor_id)
    sensor.sensor_data = sensor.sensordata_set.order_by('-timestamp')[:10]
    get_plot_data(sensor)
    return sensor

def get_plot_data(sensor):
    timestamps = [str(d.timestamp) for d in sensor.sensor_data]
    values = [d.data for d in sensor.sensor_data]

    fig, ax = plt.subplots()
    ax.plot(timestamps, values)
    ax.set_xlabel('Time')
    ax.set_ylabel(sensor.data_type)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_png = buf.getvalue()
    graph = base64.b64encode(image_png)
    sensor.image = graph.decode('utf-8')
    buf.close()

    #data_uri = buf.read().encode('base64').replace('\n', '')
    #sensor.image = format_html('<img src="data:image/png;base64,{}">', data_uri)


    '''canvas = FigureCanvas(fig)
    buf = io.BytesIO()
    canvas.print_png(buf)
    image_data = buf.getvalue()
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    image_uri = f"data:image/png;base64,{image_base64}"
    sensor.image = format_html('<img src="data:image/png;base64,{}">', image_uri)'''
    
