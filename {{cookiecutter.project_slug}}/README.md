<!--
Generated from the service template (cookiecutter) with options:
  project_slug       = {{ cookiecutter.project_slug }}
  db_schema          = {{ cookiecutter.db_schema }}
  use_kafka          = {{ cookiecutter.use_kafka }}
  use_taskiq         = {{ cookiecutter.use_taskiq }}
  use_metrics        = {{ cookiecutter.use_metrics }}
  include_example    = {{ cookiecutter.include_example }}
  include_admin_stub = {{ cookiecutter.include_admin_stub }}
Stack: Python 3.12, FastAPI, dishka, SQLAlchemy 2.0 (imperative mapping), asyncpg,
Alembic, pydantic-settings, python-json-logger, pytest, ruff, poetry, Docker.
-->

# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

FastAPI + dishka + SQLAlchemy 2.0 (imperative mapping) + Alembic
{%- if cookiecutter.use_kafka %} + FastStream (Kafka){% endif %}
{%- if cookiecutter.use_taskiq %} + taskiq (Redis){% endif %}
{%- if cookiecutter.use_metrics %} + Prometheus{% endif %}.
Clean Architecture / DDD + CQRS.

Архитектура, структура каталогов, рецепт добавления сущности и чек-лист
связывания — в [docs/architecture.md](docs/architecture.md).

## Быстрый старт

Нужны Python 3.12, poetry и Docker.

```bash
make install        # poetry install → .venv в проекте
make requirements   # requirements.txt для Docker
make infra-up       # postgres :5432{% if cookiecutter.use_taskiq %}, redis :6379{% endif %}{% if cookiecutter.use_kafka %}, kafka :9092{% endif %}
make migrate        # alembic upgrade head
make run            # API → http://localhost:8000/docs
```

`configs/prod.toml` создан при генерации из `configs/prod.toml.example`
(значения совпадают с `docker-compose.dev.yml`) и в git не попадает.
{%- if cookiecutter.use_kafka or cookiecutter.use_taskiq or cookiecutter.use_metrics %}

Остальные процессы, каждый в своём терминале:

```bash
{%- if cookiecutter.use_kafka %}
make broker            # Kafka consumers
{%- endif %}
{%- if cookiecutter.use_taskiq %}
make taskiq            # воркер фоновых задач
make taskiq-scheduler  # cron-задачи (ровно один экземпляр)
{%- endif %}
{%- if cookiecutter.use_metrics %}
make metrics           # http://localhost:8002/metrics
{%- endif %}
```
{%- endif %}

## Команды

```bash
make help              # список всех целей
make test              # pytest
make lint / format     # ruff
make migration m="add foo"
make requirements      # синхронизировать requirements.txt для Docker
```
{%- if cookiecutter.include_example %}

## Пример `Item`

Сущность `Item` проходит через все слои и служит образцом. Когда появится своя
доменка, удали её: `domain/{entities,events,exceptions}/item.py`,
`domain/interfaces/persistence/repositories/item.py`, `application/items/`,
`routes/main/items/`, модель и репозиторий в `infrastructure/persistence/db/`,
миграцию `0001_initial`
{%- if cookiecutter.use_taskiq %}, задачи `infrastructure/tasks/jobs/items.py`{% endif %}
{%- if cookiecutter.use_kafka %}, консьюмер и контракт в `presentation/broker/`{% endif %},
регистрации в DI и `registry.py`, тесты `tests/unit/test_items.py` и `fakes.py`.
{%- endif %}

## Деплой

`Dockerfile` собирает один образ; процессы запускаются скриптами из
`entrypoints/dev/` (`start.app.sh` перед стартом накатывает миграции).
Конфиг в контейнере — `configs/prod.toml` или env-переменные `SECTION__KEY`.
