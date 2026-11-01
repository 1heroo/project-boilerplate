from enum import Enum


class MiddlewareEnum(str, Enum):
    METRICS = 'METRICS'
    LOGGING = 'LOGGING'
