from pathlib import Path

from pydantic import Field{% if cookiecutter.use_taskiq %}, RedisDsn{% endif %}
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, TomlConfigSettingsSource

from src.config.logger.conf_schema import LoggingConfig
{%- if cookiecutter.use_kafka %}
from src.infrastructure.broker.conf_schema import KafkaConfig
{%- endif %}
{%- if cookiecutter.use_metrics %}
from src.infrastructure.metrics.conf_schema import PrometheusConfig
{%- endif %}
from src.infrastructure.persistence.db.conf_schema import PostgresConfig{% if cookiecutter.use_taskiq %}, RedisConfig{% endif %}
{%- if cookiecutter.use_taskiq %}
from src.infrastructure.tasks.conf_schema import TaskiqConfig
{%- endif %}
from src.presentation.rest.conf_schema import FastAPIConfig, GunicornConfig

BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = BASE_DIR / 'configs' / 'prod.toml'


class Settings(BaseSettings):
    """Aggregates the `conf_schema.py` of every module.

    Values come from `configs/prod.toml`; any key can be overridden by an env var
    with `__` as the section separator, e.g. `POSTGRES__HOST=db`.
    """

    fastapi: FastAPIConfig = Field(default_factory=FastAPIConfig)
    gunicorn: GunicornConfig = Field(default_factory=GunicornConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
{%- if cookiecutter.use_metrics %}
    prometheus: PrometheusConfig = Field(default_factory=PrometheusConfig)
{%- endif %}
    postgres: PostgresConfig = Field(default_factory=PostgresConfig)
{%- if cookiecutter.use_taskiq %}
    redis: RedisConfig = Field(default_factory=RedisConfig)
    taskiq: TaskiqConfig = Field(default_factory=TaskiqConfig)
{%- endif %}
{%- if cookiecutter.use_kafka %}
    kafka: KafkaConfig = Field(default_factory=KafkaConfig)
{%- endif %}

    model_config = {'env_nested_delimiter': '__', 'extra': 'ignore'}

    @property
    def async_psql_url(self) -> str:
        return (
            f'postgresql+asyncpg://{self.postgres.user}:{self.postgres.password.get_secret_value()}@'
            f'{self.postgres.host}:{self.postgres.port}/{self.postgres.db}'
        )
{%- if cookiecutter.use_taskiq %}

    @property
    def redis_url(self) -> str:
        return str(
            RedisDsn.build(
                scheme='redis',
                host=self.redis.host,
                port=self.redis.port,
                username=self.redis.username or None,
                password=self.redis.password.get_secret_value() if self.redis.password else None,
                path=f'/{self.redis.db}',
            )
        )
{%- endif %}

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return init_settings, env_settings, TomlConfigSettingsSource(settings_cls, CONFIG_PATH)


settings = Settings()
