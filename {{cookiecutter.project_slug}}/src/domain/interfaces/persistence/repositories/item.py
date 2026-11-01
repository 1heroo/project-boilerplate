from abc import ABC, abstractmethod
from typing import Literal

from src.domain.entities.item import Item


class IItemRepository(ABC):
    @abstractmethod
    async def get(self, item_id: int) -> Item | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_title(self, title: str) -> Item | None:
        raise NotImplementedError

    @abstractmethod
    async def get_list(
        self,
        limit: int,
        offset: int,
        search: str | None = None,
        sort_by: str | None = None,
        order: Literal['asc', 'desc'] = 'desc',
    ) -> list[Item]:
        raise NotImplementedError

    @abstractmethod
    async def count(self, search: str | None = None) -> int:
        raise NotImplementedError

    @abstractmethod
    async def create(self, item: Item) -> Item:
        raise NotImplementedError

    @abstractmethod
    async def update(self, item: Item) -> Item:
        raise NotImplementedError
