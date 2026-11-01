from dishka import Provider, Scope{% if cookiecutter.include_example %}, provide{% endif %}
{%- if cookiecutter.include_example %}

from src.domain.interfaces.persistence.repositories.item import IItemRepository
from src.infrastructure.persistence.db.repositories.item import ItemRepository
{%- endif %}


class RepositoryProvider(Provider):
    scope = Scope.REQUEST
{%- if cookiecutter.include_example %}

    item_repo = provide(ItemRepository, provides=IItemRepository)
{%- endif %}
