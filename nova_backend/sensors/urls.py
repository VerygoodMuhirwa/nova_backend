from django.urls import path
from . import views
urlpatterns= [
    path("sensorData", views.fetch_thingspeak_data_view)
    ]



