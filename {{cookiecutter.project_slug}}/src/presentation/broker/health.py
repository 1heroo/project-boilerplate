import json

from faststream.asgi import AsgiResponse, get
from faststream.asgi.types import ASGIApp, Scope


def make_health_routes() -> list[tuple[str, ASGIApp]]:
    """`/health/check` liveness: the process and its event loop are responsive."""

    @get(include_in_schema=False)
    async def liveness(scope: Scope) -> AsgiResponse:
        return AsgiResponse(
            json.dumps({'status': 'ok'}).encode(), 200, headers={'content-type': 'application/json'},
        )

    return [('/health/check', liveness)]
