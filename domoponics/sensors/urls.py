from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [

    path("", views.view_sensor_list, name="sensor_list"),

    path("<int:pk>/", views.view_sensor_detail, name="sensor_detail"),
    path("addsensor", views.view_sensor_add, name="sensor_add"),
    path('add_sensor_data/', csrf_exempt(views.view_data_sensor_add), name='add_sensor_data'),

]
