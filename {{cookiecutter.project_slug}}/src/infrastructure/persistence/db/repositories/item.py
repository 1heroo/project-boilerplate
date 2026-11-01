from typing import Literal

from sqlalchemy import func, select
from sqlalchemy.sql.elements import ColumnElement

from src.domain.entities.item import Item
from src.domain.interfaces.persistence.db import get_async_session
from src.domain.interfaces.persistence.repositories.item import IItemRepository
from src.infrastructure.persistence.db.models.item import item_table


class ItemRepository(IItemRepository):
    _SORTABLE_FIELDS = frozenset({'id', 'title', 'created_at', 'updated_at'})

    def __init__(self, session: get_async_session):
        self._session = session

    async def get(self, item_id: int) -> Item | None:
        query = select(Item).where(item_table.c.id == item_id, *self._build_conditions())
        result = await self._session.execute(query)
        return result.scalars().one_or_none()

    async def get_by_title(self, title: str) -> Item | None:
        query = select(Item).where(item_table.c.title == title, *self._build_conditions())
        result = await self._session.execute(query)
        return result.scalars().first()

    async def get_list(
        self,
        limit: int,
        offset: int,
        search: str | None = None,
        sort_by: str | None = None,
        order: Literal['asc', 'desc'] = 'desc',
    ) -> list[Item]:
        sort_column = item_table.c[sort_by if sort_by in self._SORTABLE_FIELDS else 'created_at']
        query = (
            select(Item)
            .where(*self._build_conditions(search))
            .order_by(sort_column.asc() if order == 'asc' else sort_column.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def count(self, search: str | None = None) -> int:
        query = select(func.count()).select_from(item_table).where(*self._build_conditions(search))
        result = await self._session.execute(query)
        return result.scalar_one()

    async def create(self, item: Item) -> Item:
        self._session.add(item)
        await self._session.flush()
        return item

    async def update(self, item: Item) -> Item:
        merged = await self._session.merge(item)
        await self._session.flush()
        return merged

    @staticmethod
    def _build_conditions(search: str | None = None) -> list[ColumnElement[bool]]:
        conditions: list[ColumnElement[bool]] = [item_table.c.is_deleted.is_(False)]
        if search:
            conditions.append(item_table.c.title.ilike(f'%{search}%'))
        return conditions
