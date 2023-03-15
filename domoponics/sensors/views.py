from django.shortcuts import render, redirect
from models.models import Sensor, SensorData
import io
import matplotlib.pyplot as plt
from .forms import SensorForm
import base64
from django.utils import timezone
from django.http import JsonResponse

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
    
    if request.method == 'POST':
        print("post")
        form = SensorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sensor_list')
    else:
        print('Form')
        form = SensorForm()
    return render(request, 'sensors/sensor_add_sensor.html', {'form': form})

# POST only view to add data_sensor
def view_data_sensor_add(request):
    if request.method == 'POST':
        time = timezone.now()
        sensor = Sensor.objects.get(pk=request.POST.get('sensor_id'))
        value = float(request.POST.get('value'))

        # Create a new SensorData instance
        new_data = SensorData(data=value, sensor_id=sensor, timestamp=time)
        new_data.save()
        print("Response")
        
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failure: no POST used'})







########################################
## Utils functions

# Get detail of sensor from database
# sensor_id(int) : primary key of the sensor 
def get_sensor_details(sensor_id):
    sensor = Sensor.objects.get(pk=sensor_id)
    sensor.sensor_data = sensor.sensordata_set.order_by('timestamp')[:10]
    for d in sensor.sensor_data:
        d.strftime = d.timestamp.strftime('%Y-%m-%d %H:%M')
    #get_plot_data(sensor)
    return sensor

# DEPRECATED:Return figure of data from a specific sensor, voir chart js
# Html : <img class="block-image" src="data:image/png;base64,{{ foo }}">
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

    
