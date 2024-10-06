import os
import django
from django.core.asgi import get_asgi_application

django.setup()
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from sensorapp.routing import websocket_urlpatterns

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nova_backend.settings')


# Set up ASGI application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
