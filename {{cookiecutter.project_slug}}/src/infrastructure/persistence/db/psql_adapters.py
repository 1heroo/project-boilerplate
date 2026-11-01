from collections.abc import AsyncIterable

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.config.settings import settings
from src.domain.interfaces.persistence.db import get_async_engine, get_async_session_maker


async def async_engine_impl() -> AsyncIterable[AsyncEngine]:
    engine = create_async_engine(
        settings.async_psql_url,
        pool_pre_ping=True,
        pool_size=settings.postgres.pool_size,
        max_overflow=settings.postgres.max_overflow,
        pool_recycle=7200,
    )
    yield engine
    await engine.dispose()


async def async_session_maker_impl(
    engine: get_async_engine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )


async def async_session_impl(
    session_maker: get_async_session_maker,
) -> AsyncIterable[AsyncSession]:
    async with session_maker() as session:
        yield session
