import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import threading
from sensorapp.fetch_data import fetch_data_from_thingspeak
from dotenv import load_dotenv
import sensorapp.routing

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import sensorapp.routing
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set default settings module for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nova_backend.settings')

django_asgi_app = get_asgi_application()

# Define the application
application = ProtocolTypeRouter({
    "http": django_asgi_app,
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

