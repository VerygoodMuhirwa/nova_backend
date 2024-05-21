from django.urls import path
from .views import fetch_and_receive_data

urlpatterns = [
    path('api/sensor-data/', fetch_and_receive_data, name='receive_sensor_data'),
]
