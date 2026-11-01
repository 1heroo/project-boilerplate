from dataclasses import dataclass

from src.domain.commands.base import BaseCommand, BaseCommandHandler
from src.domain.entities.item import Item
from src.domain.events.item import ItemCreatedEvent
from src.domain.exceptions.item import ItemAlreadyExistsException
from src.domain.interfaces.persistence.repositories.item import IItemRepository


@dataclass
class CreateItemCommand(BaseCommand):
    title: str
    description: str | None = None


class CreateItemCommandHandler(BaseCommandHandler[CreateItemCommand, Item]):
    def __init__(self, item_repo: IItemRepository):
        super().__init__()
        self._item_repo = item_repo

    async def handle(self, command: CreateItemCommand) -> Item:
        if await self._item_repo.get_by_title(command.title) is not None:
            raise ItemAlreadyExistsException(command.title)

        item = await self._item_repo.create(
            Item(title=command.title, description=command.description)
        )
        self.add_async_event(ItemCreatedEvent(item_id=item.id, title=item.title))
        return item
