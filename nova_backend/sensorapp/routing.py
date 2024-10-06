from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/sensor-data/$', consumers.SensorDataConsumer.as_asgi()),
    re_path(r'ws/video-data/$', consumers.VideoConsumer.as_asgi()),]
