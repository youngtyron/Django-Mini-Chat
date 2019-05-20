from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

from chat.consumers import CommonRoomConsumer

application = ProtocolTypeRouter({
	'websocket': AllowedHostsOriginValidator(
			AuthMiddlewareStack(
					URLRouter([
							url(r'^ws/chat/common/(?P<room_id>[^/]+)/$', CommonRoomConsumer),
						])
				)
		)
	})