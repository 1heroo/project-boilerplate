import logging

from dishka.integrations.taskiq import FromDishka, inject

from src.application.items.events.item_created import ITEM_CREATED_TASK
from src.application.items.queries.get_item import GetItemQuery, GetItemQueryHandler
from src.application.items.queries.list_items import ListItemsQuery, ListItemsQueryHandler
from src.infrastructure.tasks.broker import task_broker

logger = logging.getLogger(__name__)


@task_broker.task(task_name=ITEM_CREATED_TASK)
@inject(patch_module=True)
async def on_item_created(item_id: int, handler: FromDishka[GetItemQueryHandler]) -> None:
    item = await handler.handle(GetItemQuery(item_id=item_id))
    logger.info('Item created: %s', item.title, extra={'item_id': item.id})


@task_broker.task(task_name='items.report_total', schedule=[{'cron': '*/30 * * * *'}])
@inject(patch_module=True)
async def report_items_total(handler: FromDishka[ListItemsQueryHandler]) -> None:
    _, total = await handler.handle(ListItemsQuery(limit=1))
    logger.info('Items total: %s', total, extra={'items_total': total})
