from django import forms
from models.models import Sensor

class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = ['data_type', 'location', 'description']
        labales = {'data_type': 'Datatype', 'location':"Name", 'description':'Description'}
