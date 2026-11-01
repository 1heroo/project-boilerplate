"""Imperative mapping of entities to tables. Run once per process at startup."""
from src.domain.entities.item import Item
from src.infrastructure.persistence.db.models import item_table, mapper_registry

_mappers_configured = False


def run_mappers() -> None:
    global _mappers_configured
    if _mappers_configured:
        return

    mapper_registry.map_imperatively(Item, item_table)

    _mappers_configured = True
