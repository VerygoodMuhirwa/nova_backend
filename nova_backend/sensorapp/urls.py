from django.urls import path
from .views import fetch_and_receive_data
from .views import  store_sensor_data
from .views import  get_all_sensor_data
urlpatterns = [
    path('api/sensor-data/', fetch_and_receive_data, name='receive_sensor_data'),
    path('add' , store_sensor_data, name="Store sensor data"),
    path('data/all', get_all_sensor_data, name="Get all sensor data")
]
