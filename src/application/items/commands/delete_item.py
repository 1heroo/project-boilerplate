from dataclasses import dataclass
from datetime import datetime

from src.domain.commands.base import BaseCommand, BaseCommandHandler
from src.domain.exceptions.item import ItemNotFoundException
from src.domain.interfaces.persistence.repositories.item import IItemRepository


@dataclass
class DeleteItemCommand(BaseCommand):
    item_id: int


class DeleteItemCommandHandler(BaseCommandHandler[DeleteItemCommand, None]):
    """Soft delete: the row stays, `is_deleted` hides it from every read."""

    def __init__(self, item_repo: IItemRepository):
        super().__init__()
        self._item_repo = item_repo

    async def handle(self, command: DeleteItemCommand) -> None:
        item = await self._item_repo.get(command.item_id)
        if item is None:
            raise ItemNotFoundException(command.item_id)

        now = datetime.now()
        item.is_deleted = True
        item.deleted_at = now
        item.updated_at = now
        await self._item_repo.update(item)
