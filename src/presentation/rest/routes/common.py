from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, Field

ItemT = TypeVar('ItemT')


class PaginatedResponse(BaseModel, Generic[ItemT]):
    items: list[ItemT]
    total: int = Field(description='Всего записей, подходящих под фильтр')
    limit: int
    offset: int


SortOrder = Literal['asc', 'desc']
