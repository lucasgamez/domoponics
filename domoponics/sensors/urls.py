from django.urls import path

from . import views


urlpatterns = [

    path("", views.view_sensor_list, name="sensor_list"),

    path("<int:pk>/", views.view_sensor_detail, name="sensor_detail"),

]