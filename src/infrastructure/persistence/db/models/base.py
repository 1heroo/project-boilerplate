from sqlalchemy import MetaData
from sqlalchemy.orm import registry

DB_SCHEMA = 'core'

metadata = MetaData(schema=DB_SCHEMA)
mapper_registry = registry(metadata=metadata)
