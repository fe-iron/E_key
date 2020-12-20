from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from tesafe import routing as core_routing
from channels.security.websocket import AllowedHostsOriginValidator


application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                core_routing.websocket_urlpatterns
            )
        )
    ),
})
