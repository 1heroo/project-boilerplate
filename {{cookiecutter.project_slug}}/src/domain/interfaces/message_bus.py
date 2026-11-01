from abc import ABC, abstractmethod
from typing import Any

from src.domain.commands.base import BaseCommand
from src.domain.events.base import BaseAsyncEvent, BaseSyncEvent


class IMessageBus(ABC):
    @abstractmethod
    async def handle(self, command: BaseCommand) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def publish_sync(self, event: BaseSyncEvent) -> None:
        raise NotImplementedError

    @abstractmethod
    async def publish_async(self, event: BaseAsyncEvent) -> None:
        raise NotImplementedError
