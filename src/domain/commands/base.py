from dataclasses import dataclass
from typing import Generic, TypeVar

from src.domain.events.base import BaseAsyncEvent, BaseSyncEvent


@dataclass
class BaseCommand:
    pass


CT = TypeVar('CT', bound=BaseCommand)
RT = TypeVar('RT')


class BaseCommandHandler(Generic[CT, RT]):
    """Collects domain events raised while handling a command.

    `MessageBus` pulls them: sync events run inside the transaction, async events
    run after commit.
    """

    def __init__(self) -> None:
        self._sync_events: list[BaseSyncEvent] = []
        self._async_events: list[BaseAsyncEvent] = []

    def add_sync_event(self, event: BaseSyncEvent) -> None:
        self._sync_events.append(event)

    def add_async_event(self, event: BaseAsyncEvent) -> None:
        self._async_events.append(event)

    def pull_sync_events(self) -> list[BaseSyncEvent]:
        events = self._sync_events.copy()
        self._sync_events.clear()
        return events

    def pull_async_events(self) -> list[BaseAsyncEvent]:
        events = self._async_events.copy()
        self._async_events.clear()
        return events

    async def handle(self, command: CT) -> RT:
        raise NotImplementedError
