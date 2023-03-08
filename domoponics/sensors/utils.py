from models.models import Sensor

def get_sensor_details(sensor_id):
    sensor = Sensor.objects.get(pk=sensor_id)
    sensor.sensor_data = sensor.sensordata_set.order_by('-timestamp')[:10]
    return sensor