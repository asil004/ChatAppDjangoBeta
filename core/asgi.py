import os
from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator

from api.middleware import WebSocketJWTAuthMiddleware
from chat.consumer import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

ws_pattern = [
    path('ws/chatroom/<int:user_id>', ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AllowedHostsOriginValidator(
            WebSocketJWTAuthMiddleware(
                URLRouter(ws_pattern)
            )
        )
    }
)
