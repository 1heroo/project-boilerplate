from dataclasses import dataclass, field

from src.domain.events.base import BaseAsyncEvent


@dataclass
class ItemCreatedEvent(BaseAsyncEvent):
    item_id: int = field(default=0)
    title: str = field(default='')
