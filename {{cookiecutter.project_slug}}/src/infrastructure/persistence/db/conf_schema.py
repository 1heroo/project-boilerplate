from pydantic import BaseModel, SecretStr


class PostgresConfig(BaseModel):
    host: str = 'localhost'
    port: int = 5432
    user: str = 'app'
    password: SecretStr = SecretStr('app')
    db: str = 'app'
    pool_size: int = 15
    max_overflow: int = 10
{%- if cookiecutter.use_taskiq %}


class RedisConfig(BaseModel):
    host: str = 'localhost'
    port: int = 6379
    db: int = 0
    username: str | None = None
    password: SecretStr | None = None
{%- endif %}
