from django import forms
from models.models import Sensor

class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = ['dataType', 'name', 'description', 'device']
        labales = {'dataType': 'Datatype', 'name':"Name", 'description':'Description', 'device':'Device'}
