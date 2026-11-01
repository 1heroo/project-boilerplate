from dishka import Provider, Scope, provide

from src.application.items.commands.create_item import CreateItemCommandHandler
from src.application.items.commands.delete_item import DeleteItemCommandHandler
from src.application.items.commands.update_item import UpdateItemCommandHandler
from src.application.items.events.item_created import ScheduleItemCreatedTaskHandler
from src.application.items.queries.get_item import GetItemQueryHandler
from src.application.items.queries.list_items import ListItemsQueryHandler


class ServiceProvider(Provider):
    """Every query, command and event handler of the application."""

    scope = Scope.REQUEST

    get_item_handler = provide(GetItemQueryHandler)
    list_items_handler = provide(ListItemsQueryHandler)
    create_item_handler = provide(CreateItemCommandHandler)
    update_item_handler = provide(UpdateItemCommandHandler)
    delete_item_handler = provide(DeleteItemCommandHandler)
    schedule_item_created_handler = provide(ScheduleItemCreatedTaskHandler)
