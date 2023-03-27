from django_components import component
from models.models import Sensor


@component.register("graph")
class Graph(component.Component):
    # Templates inside `[your apps]/components` dir and `[project root]/components` dir will be automatically found. To customize which template to use based on context
    # you can override def get_template_name() instead of specifying the below variable.
    template_name = "graph/graph.html"

    # This component takes one parameter, a date string to show in the template
    def get_context_data(self, sensor: Sensor):
        return {
            "id": sensor.pk,
            "data": [d.data for d in sensor.sensor_data],
            "labels": [d.strftime for d in sensor.sensor_data],
            "label": sensor.dataType.unit,
            "color": sensor.dataType.color
            
        }

    class Media:
        css = "graph/graph.css"
        js = "graph/graph.js"