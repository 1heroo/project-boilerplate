from sqlalchemy import BigInteger, Boolean, Column, DateTime, String, Table, Text

from src.infrastructure.persistence.db.models.base import metadata

item_table = Table(
    't_item', metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('title', String(256), nullable=False),
    Column('description', Text),
    Column('is_deleted', Boolean, nullable=False, default=False, server_default='false'),
    Column('created_at', DateTime, nullable=False),
    Column('updated_at', DateTime, nullable=False),
    Column('deleted_at', DateTime),
)
