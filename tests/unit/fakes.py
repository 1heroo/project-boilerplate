"""In-memory doubles of domain interfaces for unit tests of handlers and the bus."""
from types import TracebackType
from typing import Literal

from src.domain.entities.item import Item
from src.domain.interfaces.persistence.repositories.item import IItemRepository
from src.domain.interfaces.persistence.unit_of_work import IUnitOfWork
from src.domain.interfaces.tasks import ITaskQueue


class FakeItemRepository(IItemRepository):
    def __init__(self) -> None:
        self.items: dict[int, Item] = {}

    async def get(self, item_id: int) -> Item | None:
        item = self.items.get(item_id)
        return item if item and not item.is_deleted else None

    async def get_by_title(self, title: str) -> Item | None:
        return next((i for i in self.items.values() if i.title == title and not i.is_deleted), None)

    async def get_list(
        self,
        limit: int,
        offset: int,
        search: str | None = None,
        sort_by: str | None = None,
        order: Literal['asc', 'desc'] = 'desc',
    ) -> list[Item]:
        alive = [i for i in self.items.values() if not i.is_deleted]
        return alive[offset:offset + limit]

    async def count(self, search: str | None = None) -> int:
        return len([i for i in self.items.values() if not i.is_deleted])

    async def create(self, item: Item) -> Item:
        item.id = len(self.items) + 1
        self.items[item.id] = item
        return item

    async def update(self, item: Item) -> Item:
        self.items[item.id] = item
        return item


class FakeUnitOfWork(IUnitOfWork):
    def __init__(self) -> None:
        self.committed = False
        self.rolled_back = False

    async def __aenter__(self) -> 'FakeUnitOfWork':
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type:
            await self.rollback()

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        self.rolled_back = True

    async def flush(self) -> None:
        return None


class FakeTaskQueue(ITaskQueue):
    def __init__(self) -> None:
        self.enqueued: list[tuple[str, dict[str, object]]] = []

    async def enqueue(self, task_name: str, **kwargs: object) -> None:
        self.enqueued.append((task_name, kwargs))
