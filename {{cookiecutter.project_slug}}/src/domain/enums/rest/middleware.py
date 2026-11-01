from enum import Enum


class MiddlewareEnum(str, Enum):
{%- if cookiecutter.use_metrics %}
    METRICS = 'METRICS'
{%- endif %}
    LOGGING = 'LOGGING'
