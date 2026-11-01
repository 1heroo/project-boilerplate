"""DI markers for the database engine, session maker and session.

The functions are never called: dishka uses them as keys, so repositories can
depend on `get_async_session` without importing the infrastructure adapters.
"""
from collections.abc import AsyncIterable

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker


def get_async_engine() -> AsyncEngine:
    raise NotImplementedError


def get_async_session_maker() -> async_sessionmaker[AsyncSession]:
    raise NotImplementedError


def get_async_session() -> AsyncIterable[AsyncSession]:
    raise NotImplementedError
