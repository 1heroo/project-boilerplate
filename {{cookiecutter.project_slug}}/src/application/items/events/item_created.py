from src.domain.events.item import ItemCreatedEvent
from src.domain.interfaces.tasks import ITaskQueue

ITEM_CREATED_TASK = 'items.on_created'


class ScheduleItemCreatedTaskHandler:
    """Runs after commit and hands the follow-up work to the background worker."""

    def __init__(self, task_queue: ITaskQueue):
        self._task_queue = task_queue

    async def __call__(self, event: ItemCreatedEvent) -> None:
        await self._task_queue.enqueue(ITEM_CREATED_TASK, item_id=event.item_id)
