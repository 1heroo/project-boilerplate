from fastapi import FastAPI

from src.domain.enums.rest.middleware import MiddlewareEnum
from src.presentation.rest.middlewares.logging import logging_middleware
from src.presentation.rest.middlewares.metrics import metrics_middleware

EXCLUDED_FROM_ACCESS_LOG = ('/metrics', '/health', '/openapi.json', '/docs', '/redoc')


def register_middlewares(app: FastAPI, middlewares: list[MiddlewareEnum] | None = None) -> None:
    for middleware in middlewares or list(MiddlewareEnum):
        match middleware:
            case MiddlewareEnum.METRICS:
                app.middleware('http')(metrics_middleware)
            case MiddlewareEnum.LOGGING:
                app.middleware('http')(logging_middleware(EXCLUDED_FROM_ACCESS_LOG))
