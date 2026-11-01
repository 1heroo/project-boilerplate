from pydantic import BaseModel


class KafkaConfig(BaseModel):
    """Topics come from config: FastStream declares subscriptions before startup."""

    bootstrap_servers: str = '127.0.0.1:9092'
    consumer_group: str = 'service'
    items_topic: str = 'items.commands'
