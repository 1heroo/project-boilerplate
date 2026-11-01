# service

Каркас бэкенд-сервиса: FastAPI + dishka + SQLAlchemy 2.0 (imperative mapping) +
Alembic + FastStream (Kafka) + taskiq (Redis) + Prometheus.
Clean Architecture / DDD + CQRS.

Архитектура, структура каталогов, рецепт добавления сущности и чек-лист
связывания — в [docs/architecture.md](docs/architecture.md).

## Быстрый старт

Нужны Python 3.12, poetry и Docker.

```bash
make install        # poetry install → .venv в проекте
make config         # configs/prod.toml из примера (значения совпадают с docker-compose.dev.yml)
make infra-up       # postgres :5432, redis :6379, kafka :9092
make migrate        # alembic upgrade head
make run            # API → http://localhost:8000/docs
```

Остальные процессы, каждый в своём терминале:

```bash
make broker            # Kafka consumers
make taskiq            # воркер фоновых задач
make taskiq-scheduler  # cron-задачи (ровно один экземпляр)
make metrics           # http://localhost:8002/metrics
```

## Команды

```bash
make help              # список всех целей
make test              # pytest
make lint / format     # ruff
make migration m="add foo"
make requirements      # синхронизировать requirements.txt для Docker
```

## Новый проект из каркаса

1. Скопировать каталог и переименовать `service` в `pyproject.toml`,
   `[fastapi] title` в `configs/prod.toml.example`, `name` в `docker-compose.dev.yml`.
2. Свою доменку добавить по рецепту из `docs/architecture.md` §5. Пример `Item`
   удалить или переделать: `domain/entities/item.py`, `application/items/`,
   `routes/main/items/`, модель, репозиторий, миграцию `0001_initial`, задачи в
   `infrastructure/tasks/jobs/items.py`, консьюмер в `presentation/broker/consumers/items.py`,
   регистрации в DI/registry.
3. Ненужные модули (Kafka / taskiq / метрики) убрать по таблице из §12.
4. Если меняется схема БД (`core`), поправить `DB_SCHEMA` в `models/base.py` и
   имя схемы в первой миграции.

## Деплой

`Dockerfile` собирает один образ; процессы запускаются скриптами из
`entrypoints/dev/` (`start.app.sh` перед стартом накатывает миграции).
Конфиг в контейнере — `configs/prod.toml` или env-переменные `SECTION__KEY`.
