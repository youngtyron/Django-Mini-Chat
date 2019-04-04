from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

from chat.consumers import NewMessagesConsumer, MessagePortionConsumer

application = ProtocolTypeRouter({
	'websocket': AllowedHostsOriginValidator(
			AuthMiddlewareStack(
					URLRouter([
							url(r'^ws/chat/newmessages/(?P<room_id>[^/]+)/$', NewMessagesConsumer),
							url(r'^ws/chat/portion/(?P<room_id>[^/]+)/$', MessagePortionConsumer)
						])
				)
		)
	})