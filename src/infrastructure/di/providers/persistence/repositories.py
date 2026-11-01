from dishka import Provider, Scope, provide

from src.domain.interfaces.persistence.repositories.item import IItemRepository
from src.infrastructure.persistence.db.repositories.item import ItemRepository


class RepositoryProvider(Provider):
    scope = Scope.REQUEST

    item_repo = provide(ItemRepository, provides=IItemRepository)
