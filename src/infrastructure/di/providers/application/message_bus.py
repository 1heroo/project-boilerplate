from dishka import AsyncContainer, Provider, Scope, provide

from src.application.message_bus import MessageBus
from src.application.registry import ASYNC_EVENT_HANDLERS, COMMAND_HANDLERS, SYNC_EVENT_HANDLERS
from src.domain.interfaces.message_bus import IMessageBus
from src.domain.interfaces.persistence.unit_of_work import IUnitOfWork


class MessageBusProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def message_bus(self, uow: IUnitOfWork, container: AsyncContainer) -> IMessageBus:
        return MessageBus(
            uow=uow,
            container=container,
            command_handlers=COMMAND_HANDLERS,
            sync_event_handlers=SYNC_EVENT_HANDLERS,
            async_event_handlers=ASYNC_EVENT_HANDLERS,
        )
