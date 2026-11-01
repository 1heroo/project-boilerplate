import logging

from dishka.integrations.faststream import FromDishka
from faststream.confluent import KafkaRouter

from src.application.items.commands.create_item import CreateItemCommand
from src.config.logger.context import log_context, new_trace_id
from src.config.settings import settings
from src.domain.interfaces.message_bus import IMessageBus
from src.presentation.broker.contracts.items import CreateItemMessage

logger = logging.getLogger(__name__)

router = KafkaRouter()


@router.subscriber(settings.kafka.items_topic, group_id=settings.kafka.consumer_group)
async def handle_create_item(message: CreateItemMessage, bus: FromDishka[IMessageBus]) -> None:
    with log_context(new_trace_id(), topic=settings.kafka.items_topic):
        item = await bus.handle(CreateItemCommand(title=message.title, description=message.description))
        logger.info('Item created from Kafka: %s', item.id, extra={'item_id': item.id})
