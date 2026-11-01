from dataclasses import dataclass
from typing import Literal

from src.domain.entities.item import Item
from src.domain.interfaces.persistence.repositories.item import IItemRepository
from src.domain.queries.base import BaseQuery


@dataclass
class ListItemsQuery(BaseQuery):
    limit: int = 20
    offset: int = 0
    search: str | None = None
    sort_by: str | None = None
    order: Literal['asc', 'desc'] = 'desc'


class ListItemsQueryHandler:
    def __init__(self, item_repo: IItemRepository):
        self._item_repo = item_repo

    async def handle(self, query: ListItemsQuery) -> tuple[list[Item], int]:
        items = await self._item_repo.get_list(
            limit=query.limit,
            offset=query.offset,
            search=query.search,
            sort_by=query.sort_by,
            order=query.order,
        )
        total = await self._item_repo.count(search=query.search)
        return items, total
