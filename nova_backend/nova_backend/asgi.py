import os
import django

# Set the Django settings module before any Django-related imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nova_backend.settings')

# Setup Django before importing other Django components
django.setup()

# Now import Django and Channels modules
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from sensorapp.routing import websocket_urlpatterns
from django.core.asgi import get_asgi_application

# Set up ASGI application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
