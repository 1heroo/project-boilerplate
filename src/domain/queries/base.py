from dataclasses import dataclass


@dataclass
class BaseQuery:
    """Read-only request. Resolved directly from DI, never goes through MessageBus."""
