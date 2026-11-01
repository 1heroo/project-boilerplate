from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class BaseSyncEvent:
    """Handled inside the same transaction, before commit."""

    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class BaseAsyncEvent:
    """Handled after commit: external side effects (broker, mail, tasks)."""

    occurred_at: datetime = field(default_factory=datetime.now)
