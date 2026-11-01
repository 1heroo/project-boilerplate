"""Registries of command and event handlers.

Every command goes to COMMAND_HANDLERS, every event to *_EVENT_HANDLERS.
Query handlers are NOT registered here; they are resolved directly via DI.
"""
{%- if cookiecutter.include_example %}
from src.application.items.commands.create_item import CreateItemCommand, CreateItemCommandHandler
from src.application.items.commands.delete_item import DeleteItemCommand, DeleteItemCommandHandler
from src.application.items.commands.update_item import UpdateItemCommand, UpdateItemCommandHandler
{%- if cookiecutter.use_taskiq %}
from src.application.items.events.item_created import ScheduleItemCreatedTaskHandler
{%- endif %}
{%- endif %}
from src.domain.commands.base import BaseCommand, BaseCommandHandler
from src.domain.events.base import BaseAsyncEvent, BaseSyncEvent
{%- if cookiecutter.include_example and cookiecutter.use_taskiq %}
from src.domain.events.item import ItemCreatedEvent
{%- endif %}

COMMAND_HANDLERS: dict[type[BaseCommand], type[BaseCommandHandler]] = {
{%- if cookiecutter.include_example %}
    CreateItemCommand: CreateItemCommandHandler,
    UpdateItemCommand: UpdateItemCommandHandler,
    DeleteItemCommand: DeleteItemCommandHandler,
{% endif -%}
}

SYNC_EVENT_HANDLERS: dict[type[BaseSyncEvent], list[type]] = {}

ASYNC_EVENT_HANDLERS: dict[type[BaseAsyncEvent], list[type]] = {
{%- if cookiecutter.include_example and cookiecutter.use_taskiq %}
    ItemCreatedEvent: [ScheduleItemCreatedTaskHandler],
{% endif -%}
}
