import logging

from faststream.confluent import KafkaBroker

from src.config.settings import settings
{%- if cookiecutter.include_example %}
from src.presentation.broker.consumers.items import router as items_router
{%- endif %}

broker = KafkaBroker(bootstrap_servers=settings.kafka.bootstrap_servers, log_level=logging.INFO)
{%- if cookiecutter.include_example %}

broker.include_router(items_router)
{%- endif %}
