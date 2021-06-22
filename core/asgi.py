"""ASGI config"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application
from django.urls import path

from chatapp.consumers import OneonOneChatConsumer, GroupChatConsumer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')


django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/chat/<slug:room_pk>/', OneonOneChatConsumer.as_asgi()),
            path('ws/group/<slug:room_pk>/', GroupChatConsumer.as_asgi())
        ])
    ),
})