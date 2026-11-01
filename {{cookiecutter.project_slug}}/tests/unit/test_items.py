import pytest
from dishka import Provider, Scope, make_async_container, provide

from src.application.items.commands.create_item import CreateItemCommand, CreateItemCommandHandler
from src.application.items.commands.delete_item import DeleteItemCommand
{%- if cookiecutter.use_taskiq %}
from src.application.items.events.item_created import ITEM_CREATED_TASK
{%- endif %}
from src.application.items.queries.get_item import GetItemQuery, GetItemQueryHandler
from src.application.message_bus import MessageBus
from src.application.registry import ASYNC_EVENT_HANDLERS, COMMAND_HANDLERS, SYNC_EVENT_HANDLERS
from src.domain.exceptions.item import ItemAlreadyExistsException, ItemNotFoundException
from src.domain.interfaces.persistence.repositories.item import IItemRepository
{%- if cookiecutter.use_taskiq %}
from src.domain.interfaces.tasks import ITaskQueue
{%- endif %}
from src.infrastructure.di.providers.application.services import ServiceProvider
from tests.unit.fakes import FakeItemRepository{% if cookiecutter.use_taskiq %}, FakeTaskQueue{% endif %}, FakeUnitOfWork


class FakesProvider(Provider):
    scope = Scope.APP

    def __init__(self, repo: FakeItemRepository{% if cookiecutter.use_taskiq %}, queue: FakeTaskQueue{% endif %}):
        super().__init__()
        self._repo = repo
{%- if cookiecutter.use_taskiq %}
        self._queue = queue
{%- endif %}

    @provide
    def item_repo(self) -> IItemRepository:
        return self._repo
{%- if cookiecutter.use_taskiq %}

    @provide
    def task_queue(self) -> ITaskQueue:
        return self._queue
{%- endif %}


@pytest.fixture
def repo() -> FakeItemRepository:
    return FakeItemRepository()
{%- if cookiecutter.use_taskiq %}


@pytest.fixture
def queue() -> FakeTaskQueue:
    return FakeTaskQueue()
{%- endif %}


@pytest.fixture
async def bus(repo: FakeItemRepository{% if cookiecutter.use_taskiq %}, queue: FakeTaskQueue{% endif %}):
    container = make_async_container(FakesProvider(repo{% if cookiecutter.use_taskiq %}, queue{% endif %}), ServiceProvider())
    async with container() as request_container:
        yield MessageBus(
            uow=FakeUnitOfWork(),
            container=request_container,
            command_handlers=COMMAND_HANDLERS,
            sync_event_handlers=SYNC_EVENT_HANDLERS,
            async_event_handlers=ASYNC_EVENT_HANDLERS,
        )
    await container.close()


async def test_create_item_rejects_duplicate_title(repo: FakeItemRepository) -> None:
    handler = CreateItemCommandHandler(item_repo=repo)
    await handler.handle(CreateItemCommand(title='first'))

    with pytest.raises(ItemAlreadyExistsException):
        await handler.handle(CreateItemCommand(title='first'))
{%- if cookiecutter.use_taskiq %}


async def test_bus_commits_and_enqueues_task_after_create(bus: MessageBus, queue: FakeTaskQueue) -> None:
    item = await bus.handle(CreateItemCommand(title='first'))

    assert bus._uow.committed
    assert queue.enqueued == [(ITEM_CREATED_TASK, {'item_id': item.id})]
{%- endif %}


async def test_missing_item_rolls_back(bus: MessageBus) -> None:
    with pytest.raises(ItemNotFoundException):
        await bus.handle(DeleteItemCommand(item_id=404))

    assert bus._uow.rolled_back
    assert not bus._uow.committed


async def test_deleted_item_is_hidden(bus: MessageBus, repo: FakeItemRepository) -> None:
    item = await bus.handle(CreateItemCommand(title='gone'))
    await bus.handle(DeleteItemCommand(item_id=item.id))

    with pytest.raises(ItemNotFoundException):
        await GetItemQueryHandler(item_repo=repo).handle(GetItemQuery(item_id=item.id))
