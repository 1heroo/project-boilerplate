import logging

from faststream.confluent import KafkaBroker

from src.config.settings import settings
from src.presentation.broker.consumers.items import router as items_router

broker = KafkaBroker(bootstrap_servers=settings.kafka.bootstrap_servers, log_level=logging.INFO)

broker.include_router(items_router)
