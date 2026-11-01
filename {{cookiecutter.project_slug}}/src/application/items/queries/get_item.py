from dataclasses import dataclass

from src.domain.entities.item import Item
from src.domain.exceptions.item import ItemNotFoundException
from src.domain.interfaces.persistence.repositories.item import IItemRepository
from src.domain.queries.base import BaseQuery


@dataclass
class GetItemQuery(BaseQuery):
    item_id: int


class GetItemQueryHandler:
    def __init__(self, item_repo: IItemRepository):
        self._item_repo = item_repo

    async def handle(self, query: GetItemQuery) -> Item:
        item = await self._item_repo.get(query.item_id)
        if item is None:
            raise ItemNotFoundException(query.item_id)
        return item
