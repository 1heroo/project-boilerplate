from dataclasses import dataclass, field

import pytest
from dishka import Provider, Scope, make_async_container, provide

from src.application.message_bus import MessageBus
from src.domain.commands.base import BaseCommand, BaseCommandHandler
from src.domain.events.base import BaseAsyncEvent, BaseSyncEvent


@dataclass
class PingCommand(BaseCommand):
    fail: bool = False


@dataclass
class PingedSync(BaseSyncEvent):
    pass


@dataclass
class PingedAsync(BaseAsyncEvent):
    pass


class Journal:
    def __init__(self) -> None:
        self.records: list[str] = []


class PingCommandHandler(BaseCommandHandler[PingCommand, str]):
    def __init__(self, journal: Journal):
        super().__init__()
        self._journal = journal

    async def handle(self, command: PingCommand) -> str:
        self.add_sync_event(PingedSync())
        self.add_async_event(PingedAsync())
        if command.fail:
            raise RuntimeError('boom')
        return 'pong'


class OnSync:
    def __init__(self, journal: Journal):
        self._journal = journal

    async def __call__(self, event: PingedSync) -> None:
        self._journal.records.append('sync')


class OnAsync:
    def __init__(self, journal: Journal):
        self._journal = journal

    async def __call__(self, event: PingedAsync) -> None:
        self._journal.records.append('async')


@dataclass
class RecordingUnitOfWork:
    journal: Journal
    calls: list[str] = field(default_factory=list)

    async def __aenter__(self) -> 'RecordingUnitOfWork':
        return self

    async def __aexit__(self, exc_type: type[BaseException] | None, *_: object) -> None:
        if exc_type:
            self.journal.records.append('rollback')

    async def commit(self) -> None:
        self.journal.records.append('commit')


class HandlersProvider(Provider):
    scope = Scope.APP

    journal = provide(Journal)
    ping = provide(PingCommandHandler)
    on_sync = provide(OnSync)
    on_async = provide(OnAsync)


@pytest.fixture
async def setup():
    container = make_async_container(HandlersProvider())
    journal = await container.get(Journal)
    bus = MessageBus(
        uow=RecordingUnitOfWork(journal),  # type: ignore[arg-type]
        container=container,
        command_handlers={PingCommand: PingCommandHandler},
        sync_event_handlers={PingedSync: [OnSync]},
        async_event_handlers={PingedAsync: [OnAsync]},
    )
    yield bus, journal
    await container.close()


async def test_sync_events_before_commit_async_after(setup: tuple[MessageBus, Journal]) -> None:
    bus, journal = setup

    assert await bus.handle(PingCommand()) == 'pong'
    assert journal.records == ['sync', 'commit', 'async']


async def test_failure_rolls_back_and_skips_async_events(setup: tuple[MessageBus, Journal]) -> None:
    bus, journal = setup

    with pytest.raises(RuntimeError):
        await bus.handle(PingCommand(fail=True))
    assert journal.records == ['rollback']
