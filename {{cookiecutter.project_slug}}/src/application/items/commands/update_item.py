from dataclasses import dataclass
from datetime import datetime

from src.domain.commands.base import BaseCommand, BaseCommandHandler
from src.domain.entities.item import Item
from src.domain.exceptions.item import ItemAlreadyExistsException, ItemNotFoundException
from src.domain.interfaces.persistence.repositories.item import IItemRepository


@dataclass
class UpdateItemCommand(BaseCommand):
    item_id: int
    title: str
    description: str | None = None


class UpdateItemCommandHandler(BaseCommandHandler[UpdateItemCommand, Item]):
    def __init__(self, item_repo: IItemRepository):
        super().__init__()
        self._item_repo = item_repo

    async def handle(self, command: UpdateItemCommand) -> Item:
        item = await self._item_repo.get(command.item_id)
        if item is None:
            raise ItemNotFoundException(command.item_id)

        same_title = await self._item_repo.get_by_title(command.title)
        if same_title is not None and same_title.id != item.id:
            raise ItemAlreadyExistsException(command.title)

        item.title = command.title
        item.description = command.description
        item.updated_at = datetime.now()
        return await self._item_repo.update(item)
