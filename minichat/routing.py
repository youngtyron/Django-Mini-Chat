from dj	ango.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack


application = ProtocolTypeRouter({
	'websocket': AllowedHostsOriginValidator(
			AuthMiddlewareStack(
					URLRouter([
						# url()
						])
				)
		)
	})