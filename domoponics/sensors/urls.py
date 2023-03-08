from django.urls import path

from . import views


urlpatterns = [

    path("", views.sensor_list, name="sensor_list"),

    #path("<int:pk>/", views.project_detail, name="project_detail"),

]