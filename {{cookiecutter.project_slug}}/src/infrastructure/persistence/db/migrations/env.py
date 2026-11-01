import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool, text
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from src.config.settings import settings
from src.infrastructure.persistence.db.models import DB_SCHEMA, metadata
from src.infrastructure.persistence.db.models.mapping import run_mappers

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

run_mappers()

target_metadata = metadata

config.set_main_option('sqlalchemy.url', settings.async_psql_url)


def include_name(name: str | None, type_: str, parent_names: dict[str, str | None]) -> bool:
    if type_ == 'schema':
        return name == DB_SCHEMA
    return True


def run_migrations_offline() -> None:
    context.configure(
        url=config.get_main_option('sqlalchemy.url'),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
        include_schemas=True,
        version_table_schema=DB_SCHEMA,
        include_name=include_name,
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Alembic creates its version table before the first migration, so the schema goes first."""
    connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS {DB_SCHEMA}'))
    connection.commit()

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        include_schemas=True,
        version_table_schema=DB_SCHEMA,
        include_name=include_name,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_async_migrations())
