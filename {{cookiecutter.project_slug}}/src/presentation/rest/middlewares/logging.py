import logging
import time
from collections.abc import Awaitable, Callable, Iterable

from fastapi import Request, Response

from src.config.logger.context import accept_trace_id, log_context

logger = logging.getLogger(__name__)

REQUEST_ID_HEADER = 'X-Request-ID'
TRACE_SCOPE_KEY = 'trace_id'

Middleware = Callable[[Request, Callable[[Request], Awaitable[Response]]], Awaitable[Response]]


def logging_middleware(excluded_paths: Iterable[str]) -> Middleware:
    """One access record per request: method, route, status, duration — never bodies.

    The trace id comes from `X-Request-ID` or is generated, is returned in the same
    header and is kept in the ASGI scope for the outermost 500 handler.
    """
    excluded = tuple(excluded_paths)

    async def logging_middleware_impl(
        request: Request, call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        trace_id = accept_trace_id(request.headers.get(REQUEST_ID_HEADER))
        request.scope[TRACE_SCOPE_KEY] = trace_id
        with log_context(trace_id):
            start = time.perf_counter()
            status_code = 500
            try:
                response = await call_next(request)
                status_code = response.status_code
                response.headers[REQUEST_ID_HEADER] = trace_id
                return response
            finally:
                if not request.url.path.startswith(excluded):
                    route = request.scope.get('route')
                    logger.info(
                        'HTTP %s %s %s', request.method, request.url.path, status_code,
                        extra={
                            'http_method': request.method,
                            'http_route': getattr(route, 'path', None),
                            'http_status': status_code,
                            'duration_ms': round((time.perf_counter() - start) * 1000, 1),
                        },
                    )

    return logging_middleware_impl
