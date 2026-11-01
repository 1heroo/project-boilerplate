import time
from collections.abc import Awaitable, Callable

from fastapi import Request, Response

from src.infrastructure.metrics.instruments.http import observe_request


async def metrics_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Count and time every request by route template; an unhandled error counts as 500."""
    start = time.perf_counter()
    status_code = 500
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        route = request.scope.get('route')
        observe_request(
            request.method, getattr(route, 'path', None), status_code, time.perf_counter() - start,
        )
