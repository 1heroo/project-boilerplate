# Архитектура сервиса

```
presentation (FastAPI routes, FastStream consumers, Pydantic schemas)
      |
      v
application  (commands, queries, event handlers, MessageBus, registry)
      |
      v
domain       (entities, I*Repository, IUnitOfWork, IMessageBus, CoreException)
      ^
      |
infrastructure (SQLAlchemy Table() + mapping, repositories, UoW, dishka providers,
                taskiq, Kafka publishers, Prometheus, external clients)
```

Каркас бэкенд-сервиса: **Clean Architecture / DDD + CQRS**. Доменка у каждого
проекта своя, а слои, их связывание и соглашения ниже остаются неизменными.
{% if cookiecutter.include_example %}Сущность `Item` в каркасе — образец, который проходит через все слои. Его можно
скопировать под свою сущность или удалить.
{% endif %}
Дерево в §2 — полная схема каркаса. Модули, отключённые при генерации проекта,
в нём отсутствуют; если понадобятся — переносятся из шаблона по той же схеме.

---

## 1. Правила, которые нельзя нарушать

1. **Зависимости направлены внутрь.** `presentation → application → domain`,
   `infrastructure → domain`. `domain` не импортирует другие слои и не знает про
   FastAPI, Pydantic, Kafka, taskiq (исключение — маркеры сессии в
   `domain/interfaces/persistence/db.py`, это ключи DI).
2. **Domain — чистый Python.** Сущности — `@dataclass`, интерфейсы — `ABC`.
   Таблицы описаны отдельно через `Table()`, связка — imperative mapping.
3. **Application работает только с абстракциями** (`I*Repository`, `IMessageBus`,
   `IUnitOfWork`, `ITaskQueue`, `I*Client`) — не с реализациями.
4. **Pydantic только в `presentation`** (REST-схемы и контракты сообщений брокера).
   Между слоями ходят entity, DTO, команды и запросы.
5. **CQRS.**
   - Query (чтение) → хендлер берётся из DI прямо в роутере: `FromDishka[XQueryHandler]`.
   - Command (мутация) → `FromDishka[IMessageBus]` и `bus.handle(XCommand(...))`.
     Транзакция (UoW) и доменные события — внутри bus.
6. **Транзакцией владеет `MessageBus` + `UnitOfWork`.** Репозиторий делает `flush()`,
   НЕ `commit()`.
7. **Фильтрация, сортировка, пагинация — в SQL внутри репозитория.** Без циклов в
   Python и без N+1. Сортируемые поля — по белому списку `_SORTABLE_FIELDS`.
8. **Никаких `try/except` в бизнес-коде и роутерах.** Бросаем наследника
   `CoreException(code, message)`, центральный handler мапит `code → HTTP`.
9. **DI — только dishka** (`DishkaRoute`, `FromDishka`), не `Depends()`.
10. **Импорты только абсолютные** (`from src...`).

---

## 2. Структура

```
src/
├── domain/                         # Ядро, без внешних зависимостей
│   ├── entities/                   # @dataclass сущности
│   ├── commands/base.py            # BaseCommand, BaseCommandHandler (копит sync/async события)
│   ├── queries/base.py             # BaseQuery
│   ├── events/                     # BaseSyncEvent, BaseAsyncEvent + доменные события
│   ├── exceptions/                 # CoreException, codes.py, исключения по сущностям
│   ├── enums/                      # бизнес-перечисления; rest/ — enum'ы handlers/middlewares
│   ├── interfaces/                 # ABC-абстракции
│   │   ├── persistence/            #   unit_of_work, db (DI-маркеры), repositories/
│   │   ├── clients/                #   I<External>Client
│   │   ├── application/            #   интерфейсы прикладных сервисов (auth и т.п.)
│   │   ├── message_bus.py
│   │   └── tasks.py                #   ITaskQueue
│   ├── services/                   # чистая доменная логика без I/O
│   └── value_objects/
│
├── application/                    # Use cases. Знает только domain
│   ├── <context>/                  # напр. items/ — ограниченный контекст
│   │   ├── commands/               #   один файл = Command + Handler
│   │   ├── queries/                #   один файл = Query + Handler
│   │   ├── events/                 #   обработчики доменных событий
│   │   └── dto/                    #   проекции (не entity, не Pydantic)
│   ├── admin/                      # заготовка под админ-контекст (пусто)
│   ├── common/                     # кросс-контекстные сервисы
│   ├── message_bus.py              # MessageBus
│   └── registry.py                 # COMMAND_HANDLERS / SYNC_ / ASYNC_EVENT_HANDLERS
│
├── infrastructure/                 # Реализации абстракций
│   ├── persistence/db/
│   │   ├── models/                 #   Table() + base.py (схема) + mapping.py (run_mappers)
│   │   ├── repositories/           #   реализации I*Repository
│   │   ├── migrations/             #   Alembic (versions/)
│   │   ├── unit_of_work.py
│   │   ├── psql_adapters.py        #   engine / session_maker / session
│   │   └── conf_schema.py          #   PostgresConfig, RedisConfig
│   ├── di/
│   │   ├── ioc_container.py        #   один контейнер на все процессы
│   │   └── providers/              #   persistence/ application/ clients/ tasks.py
│   ├── broker/                     # Kafka-продюсеры/паблишеры + KafkaConfig
│   ├── tasks/                      # taskiq: broker, queue (ITaskQueue), jobs/, health_server
│   ├── metrics/                    # Prometheus multiprocess: instruments/, collectors/, scrape
│   ├── clients/                    # HTTP/SMTP/внешние интеграции
│   └── services/                   # тяжёлая инфраструктурная логика (Excel, парсеры)
│
├── presentation/                   # Вход/выход. Pydantic только здесь
│   ├── rest/
│   │   ├── routes/
│   │   │   ├── default/            #   /health/check
│   │   │   ├── main/<section>/     #   публичный API /api/v1: routes.py + schemas.py
│   │   │   ├── admin/              #   заготовка под админ-роуты (пусто)
│   │   │   └── common.py           #   PaginatedResponse и общие схемы
│   │   ├── middlewares/            #   logging (trace_id), metrics, forwarded_prefix
│   │   ├── exception_handlers/     #   domain / validation / system
│   │   └── conf_schema.py          #   FastAPIConfig, GunicornConfig
│   └── broker/                     # FastStream: consumers/, contracts/, router_register, health
│
├── config/                         # settings.py (TOML + env), logger/
├── main.py                         # публичный API             :8000
├── metrics.py                      # /metrics                  :8002
├── broker.py                       # Kafka consumers (FastStream)
├── _taskiq.py                      # taskiq worker             health :8003
└── _scheduler.py                   # taskiq scheduler (один экземпляр)
```

### Роуты — по секциям

Каждая секция (ресурс) — **своя папка-пакет** с `routes.py` и `schemas.py`.
В `routes.py` объявлен `router = APIRouter(prefix=..., tags=['<Секция>'], route_class=DishkaRoute)`.
Пакеты лежат плоско, рядом друг с другом, и собираются в `__init__.py` области:
`bind_main_routes()` / `bind_admin_routes()` подключают их через `include_router`.
Разнородные эндпоинты в одном роутере не держим.

---

## 3. Процессы

Один код — несколько процессов (в Kubernetes это отдельные deployment'ы):

| Entry point | Процесс | Локально | Health |
|---|---|---|---|
| `src/main.py` | публичный API | `make run` | `:8000/health/check` |
{%- if cookiecutter.use_metrics %}
| `src/metrics.py` | агрегатор Prometheus | `make metrics` | `:8002/health/check` |
{%- endif %}
{%- if cookiecutter.use_kafka %}
| `src/broker.py` | Kafka consumers | `make broker` | `:8004/health/check` (порт из `--port`) |
{%- endif %}
{%- if cookiecutter.use_taskiq %}
| `src/_taskiq.py` | воркер фоновых задач | `make taskiq` | `:8003/health/check` |
| `src/_scheduler.py` | планировщик (cron-задачи) | `make taskiq-scheduler` | — |
{%- endif %}

Каждый entry point делает: `setup_logging()` → `run_mappers()` → регистрация
handlers/middlewares/роутеров → `setup_dishka(get_async_container(), app)`.
Health — только liveness: зависимости не проверяет, иначе при падении общей БД
k8s будет по кругу перезапускать исправные поды.

---

{%- if cookiecutter.include_example %}
## 4. Поток команды (пример `Item`)

```
POST /api/v1/items
  → routes.py: bus.handle(CreateItemCommand)
    → MessageBus: async with UoW
        → CreateItemCommandHandler: repo.create() (flush) + add_async_event(ItemCreatedEvent)
        → sync-события → commit
    → после commit: ItemCreatedEvent → ScheduleItemCreatedTaskHandler → ITaskQueue.enqueue
      → taskiq worker: on_item_created (trace_id тот же, что у HTTP-запроса)
```

Kafka-путь — тот же bus: `presentation/broker/consumers/items.py` валидирует
сообщение Pydantic-контрактом и вызывает `bus.handle(CreateItemCommand(...))`.

{%- endif %}
---

## 5. Рецепт: новая сущность `Foo`

1. **Domain**
   - `domain/entities/foo.py` — `@dataclass Foo` (обязательные поля первыми; `id`,
     `is_deleted`, `created_at`, `updated_at` — с дефолтами; связи — `repr=False`).
   - `domain/interfaces/persistence/repositories/foo.py` — `IFooRepository(ABC)`.
   - `domain/exceptions/foo.py` — `FooNotFoundException(CoreException)` и т.п.
   - при необходимости `domain/events/foo.py`, `domain/enums/foo.py`.
2. **Infrastructure**
   - `infrastructure/persistence/db/models/foo.py` — `foo_table = Table(...)`,
     экспорт в `models/__init__.py`.
   - `models/mapping.py` → `mapper_registry.map_imperatively(Foo, foo_table)`.
   - `infrastructure/persistence/db/repositories/foo.py` — `FooRepository(IFooRepository)`.
   - `make migration m="add foo"` → проверить сгенерированный файл → `make migrate`.
3. **Application**
   - `application/<context>/queries/{get_foo,list_foos}.py` — Query + Handler.
   - `application/<context>/commands/{create,update,delete}_foo.py` — Command + Handler.
   - события → `application/<context>/events/`.
4. **Регистрация** (см. чек-лист ниже).
5. **Presentation**
   - `presentation/rest/routes/main/foos/schemas.py` + `routes.py`.
   - подключить в `routes/main/__init__.py`.

---

## 6. Чек-лист связывания

Компоненты не находятся автоматически. Пропуск → `NoFactoryError` (dishka) или
`No handler for command`.

- [ ] Репозиторий → `di/providers/persistence/repositories.py`.
- [ ] **Каждый** Query-, Command- и Event-хендлер → `di/providers/application/services.py`.
- [ ] Команда → `COMMAND_HANDLERS` в `application/registry.py` (Query туда НЕ добавляются).
- [ ] Событие → `SYNC_EVENT_HANDLERS` / `ASYNC_EVENT_HANDLERS`.
- [ ] Новый провайдер → `ioc_container.default_providers()`.
- [ ] Таблица → `models/__init__.py` + `models/mapping.py`.
- [ ] Роутер → `bind_*_routes()`.
- [ ] Kafka-консьюмер → `presentation/broker/router_register.py`.
- [ ] taskiq-задача → модуль импортируется в `infrastructure/tasks/jobs/__init__.py`.
- [ ] Настройка → `conf_schema.py` модуля + поле в `Settings` + `configs/prod.toml.example`.

---

## 7. Конфигурация

- `Settings` (`src/config/settings.py`) собирает `conf_schema.py` всех модулей.
- Источники по приоритету: env (`SECTION__KEY`, напр. `POSTGRES__HOST=db`) → `configs/prod.toml`.
- Секреты — `SecretStr`, достаются через `.get_secret_value()`.
- Производные значения (DSN, Redis URL) — `@property` на `Settings`.

## 8. Логирование

- stdlib `logging` + `python-json-logger`, только stdout. Формат `json` или `plain` из конфига.
- `trace_id` через `contextvars` (`config/logger/context.py`): HTTP берёт его из
  `X-Request-ID` или генерирует, taskiq переносит в метках задачи, Kafka-консьюмер
  заводит новый на каждое сообщение. Секреты в `extra` маскируются форматтером.

## 9. Ошибки

- Бизнес-ошибки — наследники `CoreException` в `domain/exceptions/`, коды — в `codes.py`.
- `presentation/rest/exception_handlers/domain.py` мапит `code → HTTP` и отдаёт
  `{"code": ..., "message": ...}`. Сообщения для пользователя — на русском.

## 10. Стиль кода

- Python 3.12, тайпхинты везде, `str | None` (не `Optional`). `Any` — только там, где без него нельзя.
- Инлайновых `#`-комментариев по умолчанию нет: замысел объясняют имена и docstring
  класса/модуля. `#` — только на неочевидное «почему». Комментарии и docstring — латиницей.
- Тесты — на бизнес-логику, контракты и нетривиальные алгоритмы. Обвязку (конфиг,
  DI-проводка, middleware) проверяем прогоном и живым запуском. Шаблон — `tests/unit/`
  (in-memory фейки интерфейсов + реальный `MessageBus`).
- Источник истины по стилю — `ruff` (`make lint`).

---

## 11. Красные флаги

- Импорт FastAPI / Pydantic / taskiq / FastStream в `domain/` или `application/`.
- Pydantic-модель вне `presentation/`.
- `commit()` в репозитории; бизнес-логика или SQL в роутере.
- Мутация из роутера мимо `MessageBus`.
- `try/except` вокруг бизнес-вызовов.
- Фильтрация/сортировка циклами в Python; N+1.
- Реализация (а не интерфейс) в сигнатуре хендлера.
- Декларативная ORM-модель вместо `Table()` + imperative mapping.
- Хендлер/репозиторий добавлен, но не зарегистрирован в DI/registry.

---

## 12. Если модуль не нужен

| Убрать | Что удалить |
|---|---|
{%- if cookiecutter.use_kafka %}
| Kafka | `src/broker.py`, `presentation/broker/`, `infrastructure/broker/`, поле `kafka` в `Settings`, зависимости `faststream`, `confluent-kafka`, сервис `kafka` в compose |
{%- endif %}
{%- if cookiecutter.use_taskiq %}
| taskiq | `src/_taskiq.py`, `src/_scheduler.py`, `infrastructure/tasks/`, `TasksProvider`, `ITaskQueue` и его хендлеры, поля `redis`/`taskiq`, зависимости `taskiq*`, `redis` |
{%- endif %}
{%- if cookiecutter.use_metrics %}
| Метрики | `src/metrics.py`, `infrastructure/metrics/`, `MiddlewareEnum.METRICS`, `presentation/rest/middlewares/metrics.py`, поле `prometheus`, `prometheus-client` |
{%- endif %}

Админка: {% if cookiecutter.include_admin_stub %}под неё заготовлены пустые пакеты `application/admin/` и
`presentation/rest/routes/admin/`. {% endif %}Когда понадобится — отдельный entry point
`src/admin.py` по образцу `main.py` с `bind_admin_routes()`, плюс авторизация
через интерфейс в `domain/interfaces/application/`.
