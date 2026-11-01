from typing import Any

from dishka import AsyncContainer

from src.domain.commands.base import BaseCommand, BaseCommandHandler
from src.domain.events.base import BaseAsyncEvent, BaseSyncEvent
from src.domain.interfaces.message_bus import IMessageBus
from src.domain.interfaces.persistence.unit_of_work import IUnitOfWork


class MessageBus(IMessageBus):
    """Owns the transaction boundary of a command and dispatches its events."""

    def __init__(
        self,
        uow: IUnitOfWork,
        container: AsyncContainer,
        command_handlers: dict[type[BaseCommand], type[BaseCommandHandler]],
        sync_event_handlers: dict[type[BaseSyncEvent], list[type]],
        async_event_handlers: dict[type[BaseAsyncEvent], list[type]],
    ):
        self._uow = uow
        self._container = container
        self._command_handlers = command_handlers
        self._sync_event_handlers = sync_event_handlers
        self._async_event_handlers = async_event_handlers

    async def handle(self, command: BaseCommand) -> Any:
        handler_class = self._command_handlers.get(type(command))
        if handler_class is None:
            raise ValueError(f'No handler for command {type(command).__name__}')

        handler: BaseCommandHandler = await self._container.get(handler_class)

        async with self._uow:
            result = await handler.handle(command)
            for event in handler.pull_sync_events():
                await self.publish_sync(event)
            await self._uow.commit()

        for event in handler.pull_async_events():
            await self.publish_async(event)
        return result

    async def publish_sync(self, event: BaseSyncEvent) -> None:
        for handler_class in self._sync_event_handlers.get(type(event), []):
            handler = await self._container.get(handler_class)
            await handler(event)

    async def publish_async(self, event: BaseAsyncEvent) -> None:
        for handler_class in self._async_event_handlers.get(type(event), []):
            handler = await self._container.get(handler_class)
            await handler(event)
