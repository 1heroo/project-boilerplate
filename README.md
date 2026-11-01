# Service template

Шаблон cookiecutter для бэкенд-сервисов: Clean Architecture / DDD + CQRS на
FastAPI, dishka, SQLAlchemy 2.0 (imperative mapping), Alembic, pydantic-settings.
По выбору подключаются Kafka (FastStream), фоновые задачи (taskiq + Redis) и
Prometheus-метрики.

## Создать проект

```bash
uvx cookiecutter gh:1heroo/project-boilerplate
# или из локального клона: uvx cookiecutter ./project-boilerplate
```

Cookiecutter задаст вопросы (развилки):

| Параметр | По умолчанию | Что делает |
|---|---|---|
| `project_name` | My Service | Название, title API |
| `project_slug` | из названия | Каталог, имя пакета в pyproject, compose project, consumer group |
| `description`, `author` | — | Метаданные pyproject и README |
| `db_schema` | `core` | Схема Postgres для таблиц сервиса и `alembic_version` |
| `timezone` | `Asia/Bishkek` | `TZ` в Dockerfile |
| `use_kafka` | да | `src/broker.py`, FastStream-консьюмеры, Kafka в compose |
| `use_taskiq` | да | Воркер и планировщик taskiq, Redis, `ITaskQueue` |
| `use_metrics` | да | Отдельная metrics-апка, HTTP-метрики, multiprocess Prometheus |
| `include_example` | нет | Справочная сущность `Item` через все слои: CRUD, событие → задача, Kafka-консьюмер, тесты. Включать, чтобы посмотреть образец |
| `include_admin_stub` | да | Пустые пакеты `application/admin/`, `routes/admin/` |

Без вопросов, с параметрами:

```bash
uvx cookiecutter --no-input gh:1heroo/project-boilerplate \
  project_name="Payments Reports" use_kafka=false
```

Дальше — `README.md` сгенерированного проекта (`make install requirements`,
`make infra-up migrate run`). Схема слоёв, рецепт новой сущности и чек-лист
связывания — в его `docs/architecture.md`.

## Как устроен шаблон

- `{{cookiecutter.project_slug}}/` — сам проект. Общие файлы (settings, DI,
  registry, роуты, pyproject, Makefile, compose, конфиг) содержат Jinja-условия
  по опциям.
- `hooks/pre_gen_project.py` — проверяет слаг и имя схемы.
- `hooks/post_gen_project.py` — удаляет файлы и каталоги отключённых модулей,
  создаёт `configs/prod.toml` из примера.
- `scripts/check_template.sh` — генерирует все 32 комбинации опций и для каждой
  гоняет ruff, pytest, импорт entry points и проверяет, что не осталось следов
  отключённых модулей и неотрендеренного Jinja. Запускать после любой правки шаблона.

## Правка шаблона

- Новый опциональный модуль: добавить флаг в `cookiecutter.json` (+ `__prompts__`),
  его файлы — в списки `hooks/post_gen_project.py`, точки подключения обернуть в
  `{%- if cookiecutter.<flag> %}`, проверку следов — в `scripts/check_template.sh`.
- Файлы, где есть `{{`/`{%` не для Jinja, — в `_copy_without_render`.
- Markdown с большим количеством кириллицы в первом килобайте cookiecutter
  принимает за бинарный и не рендерит: поэтому в начале `README.md` и
  `docs/architecture.md` стоит ASCII-блок (опции генерации, схема слоёв).
