from dishka import Provider, Scope{% if cookiecutter.include_example %}, provide{% endif %}
{%- if cookiecutter.include_example %}

from src.application.items.commands.create_item import CreateItemCommandHandler
from src.application.items.commands.delete_item import DeleteItemCommandHandler
from src.application.items.commands.update_item import UpdateItemCommandHandler
{%- if cookiecutter.use_taskiq %}
from src.application.items.events.item_created import ScheduleItemCreatedTaskHandler
{%- endif %}
from src.application.items.queries.get_item import GetItemQueryHandler
from src.application.items.queries.list_items import ListItemsQueryHandler
{%- endif %}


class ServiceProvider(Provider):
    """Every query, command and event handler of the application."""

    scope = Scope.REQUEST
{%- if cookiecutter.include_example %}

    get_item_handler = provide(GetItemQueryHandler)
    list_items_handler = provide(ListItemsQueryHandler)
    create_item_handler = provide(CreateItemCommandHandler)
    update_item_handler = provide(UpdateItemCommandHandler)
    delete_item_handler = provide(DeleteItemCommandHandler)
{%- if cookiecutter.use_taskiq %}
    schedule_item_created_handler = provide(ScheduleItemCreatedTaskHandler)
{%- endif %}
{%- endif %}
