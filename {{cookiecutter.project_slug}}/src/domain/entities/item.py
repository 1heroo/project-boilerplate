from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Item:
    """Example entity. Replace with the real domain of the service."""

    title: str
    description: str | None = None
    id: int | None = None
    is_deleted: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: datetime | None = None
