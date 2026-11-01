from dishka import Provider, Scope, provide

from src.domain.interfaces.persistence.db import get_async_engine, get_async_session, get_async_session_maker
from src.domain.interfaces.persistence.unit_of_work import IUnitOfWork
from src.infrastructure.persistence.db.psql_adapters import (
    async_engine_impl,
    async_session_impl,
    async_session_maker_impl,
)
from src.infrastructure.persistence.db.unit_of_work import UnitOfWork


class DBProvider(Provider):
    async_engine = provide(
        source=staticmethod(async_engine_impl), provides=get_async_engine, scope=Scope.APP,
    )
    async_session_maker = provide(
        source=staticmethod(async_session_maker_impl), provides=get_async_session_maker, scope=Scope.APP,
    )
    async_session = provide(
        source=staticmethod(async_session_impl), provides=get_async_session, scope=Scope.REQUEST,
    )

    @provide(provides=IUnitOfWork, scope=Scope.REQUEST)
    async def unit_of_work(self, session: get_async_session) -> UnitOfWork:
        return UnitOfWork(session=session)
