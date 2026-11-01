from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Query, status

from src.application.items.commands.create_item import CreateItemCommand
from src.application.items.commands.delete_item import DeleteItemCommand
from src.application.items.commands.update_item import UpdateItemCommand
from src.application.items.queries.get_item import GetItemQuery, GetItemQueryHandler
from src.application.items.queries.list_items import ListItemsQuery, ListItemsQueryHandler
from src.domain.interfaces.message_bus import IMessageBus
from src.presentation.rest.routes.common import PaginatedResponse, SortOrder
from src.presentation.rest.routes.main.items.schemas import (
    ItemCreateRequest,
    ItemResponse,
    ItemUpdateRequest,
)

router = APIRouter(prefix='/items', tags=['Items'], route_class=DishkaRoute)


@router.get('', response_model=PaginatedResponse[ItemResponse], summary='Список элементов')
async def list_items(
    handler: FromDishka[ListItemsQueryHandler],
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    search: str | None = Query(default=None, max_length=256),
    sort_by: str | None = Query(default=None, description='id, title, created_at, updated_at'),
    order: SortOrder = Query(default='desc'),
) -> PaginatedResponse[ItemResponse]:
    items, total = await handler.handle(
        ListItemsQuery(limit=limit, offset=offset, search=search, sort_by=sort_by, order=order)
    )
    return PaginatedResponse[ItemResponse](
        items=[ItemResponse.model_validate(item) for item in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get('/{item_id}', response_model=ItemResponse, summary='Получить элемент')
async def get_item(item_id: int, handler: FromDishka[GetItemQueryHandler]) -> ItemResponse:
    item = await handler.handle(GetItemQuery(item_id=item_id))
    return ItemResponse.model_validate(item)


@router.post(
    '', response_model=ItemResponse, status_code=status.HTTP_201_CREATED, summary='Создать элемент',
)
async def create_item(body: ItemCreateRequest, bus: FromDishka[IMessageBus]) -> ItemResponse:
    item = await bus.handle(CreateItemCommand(title=body.title, description=body.description))
    return ItemResponse.model_validate(item)


@router.put('/{item_id}', response_model=ItemResponse, summary='Обновить элемент')
async def update_item(
    item_id: int, body: ItemUpdateRequest, bus: FromDishka[IMessageBus],
) -> ItemResponse:
    item = await bus.handle(
        UpdateItemCommand(item_id=item_id, title=body.title, description=body.description)
    )
    return ItemResponse.model_validate(item)


@router.delete('/{item_id}', status_code=status.HTTP_204_NO_CONTENT, summary='Удалить элемент')
async def delete_item(item_id: int, bus: FromDishka[IMessageBus]) -> None:
    await bus.handle(DeleteItemCommand(item_id=item_id))
