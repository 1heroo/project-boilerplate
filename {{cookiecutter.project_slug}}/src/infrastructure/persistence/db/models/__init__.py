from src.infrastructure.persistence.db.models.base import DB_SCHEMA, mapper_registry, metadata
{%- if cookiecutter.include_example %}
from src.infrastructure.persistence.db.models.item import item_table
{%- endif %}

__all__ = ['DB_SCHEMA', {% if cookiecutter.include_example %}'item_table', {% endif %}'mapper_registry', 'metadata']
