from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

from chat.consumers import ChatConsumer

application = ProtocolTypeRouter({
	'websocket': AllowedHostsOriginValidator(
			AuthMiddlewareStack(
					URLRouter([
							url(r'^ws/chat/(?P<room_id>[^/]+)/$', ChatConsumer)
						])
				)
		)
	})