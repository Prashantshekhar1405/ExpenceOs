"""
ASGI config for ExpenseOs project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter , URLRouter
from django.core.asgi import get_asgi_application
from notifications.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ExpenseOs.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http" : django_asgi_app,
    "websocket" : URLRouter(websocket_urlpatterns),
})
