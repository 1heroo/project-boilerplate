import asyncio

from taskiq.kicker import AsyncKicker

from src.domain.interfaces.tasks import ITaskQueue
from src.infrastructure.tasks.broker import task_broker


class TaskiqTaskQueue(ITaskQueue):
    """Kicks tasks by name; the broker starts on the first enqueue.

    Lazy start keeps the API bootable while Redis is down: only enqueueing needs it.
    """

    def __init__(self) -> None:
        self._started = False
        self._lock = asyncio.Lock()

    async def enqueue(self, task_name: str, **kwargs: object) -> None:
        await self._ensure_started()
        await AsyncKicker(task_name=task_name, broker=task_broker, labels={}).kiq(**kwargs)

    async def _ensure_started(self) -> None:
        if self._started:
            return
        async with self._lock:
            if not self._started:
                if not task_broker.is_worker_process:
                    await task_broker.startup()
                self._started = True
