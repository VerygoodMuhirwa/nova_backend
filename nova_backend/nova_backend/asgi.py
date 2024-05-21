import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import sensorapp.routing
import threading
from sensorapp.fetch_data import fetch_data_from_thingspeak

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nova_backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            sensorapp.routing.websocket_urlpatterns
        )
    ),
})

# Start the ThingSpeak data fetching in a background thread
def start_fetching_data():
    channel_id = '2511877'
    read_api_key = 'YX33ECEWQJ1PXWKJ'
    fetch_data_from_thingspeak(channel_id, read_api_key)

thread = threading.Thread(target=start_fetching_data)
thread.daemon = True
thread.start()
