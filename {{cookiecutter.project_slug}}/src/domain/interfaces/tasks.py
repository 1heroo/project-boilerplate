from abc import ABC, abstractmethod


class ITaskQueue(ABC):
    """Hands work over to the background worker without the application knowing taskiq."""

    @abstractmethod
    async def enqueue(self, task_name: str, **kwargs: object) -> None:
        raise NotImplementedError
