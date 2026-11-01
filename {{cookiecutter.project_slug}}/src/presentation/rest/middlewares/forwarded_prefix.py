from typing import Any


class ForwardedPrefixMiddleware:
    """Sets `root_path` from `X-Forwarded-Prefix`, so the app works behind an ingress subpath."""

    def __init__(self, app: Any) -> None:
        self.app = app

    async def __call__(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
        if scope['type'] in ('http', 'websocket'):
            prefix = dict(scope['headers']).get(b'x-forwarded-prefix')
            if prefix:
                scope['root_path'] = prefix.decode()
        await self.app(scope, receive, send)
