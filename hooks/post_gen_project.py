"""Removes the modules the user opted out of and prints the next steps."""
import shutil
from pathlib import Path

USE_KAFKA = {{ cookiecutter.use_kafka }}
USE_TASKIQ = {{ cookiecutter.use_taskiq }}
USE_METRICS = {{ cookiecutter.use_metrics }}
INCLUDE_EXAMPLE = {{ cookiecutter.include_example }}
INCLUDE_ADMIN_STUB = {{ cookiecutter.include_admin_stub }}

KAFKA = [
    'src/broker.py',
    'src/presentation/broker',
    'src/infrastructure/broker',
    'entrypoints/dev/start.broker.sh',
]
TASKIQ = [
    'src/_taskiq.py',
    'src/_scheduler.py',
    'src/infrastructure/tasks',
    'src/infrastructure/di/providers/tasks.py',
    'src/domain/interfaces/tasks.py',
    'src/application/items/events/item_created.py',
    'entrypoints/dev/start.taskiq.sh',
    'entrypoints/dev/start.scheduler.sh',
]
METRICS = [
    'src/metrics.py',
    'src/infrastructure/metrics',
    'src/presentation/rest/middlewares/metrics.py',
    'entrypoints/dev/start.metrics.sh',
]
EXAMPLE = [
    'src/domain/entities/item.py',
    'src/domain/events/item.py',
    'src/domain/exceptions/item.py',
    'src/domain/interfaces/persistence/repositories/item.py',
    'src/application/items',
    'src/infrastructure/persistence/db/models/item.py',
    'src/infrastructure/persistence/db/repositories/item.py',
    'src/infrastructure/persistence/db/migrations/versions/0001_initial.py',
    'src/infrastructure/tasks/jobs/items.py',
    'src/presentation/rest/routes/main/items',
    'src/presentation/broker/consumers/items.py',
    'src/presentation/broker/contracts/items.py',
    'tests/unit/test_items.py',
    'tests/unit/fakes.py',
]
ADMIN_STUB = [
    'src/application/admin',
    'src/presentation/rest/routes/admin',
]


def remove(paths: list[str]) -> None:
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()


if not USE_KAFKA:
    remove(KAFKA)
if not USE_TASKIQ:
    remove(TASKIQ)
if not USE_METRICS:
    remove(METRICS)
if not INCLUDE_EXAMPLE:
    remove(EXAMPLE)
    Path('src/infrastructure/persistence/db/migrations/versions/.gitkeep').touch()
if not INCLUDE_ADMIN_STUB:
    remove(ADMIN_STUB)

Path('configs/prod.toml').write_text(Path('configs/prod.toml.example').read_text())

print(
    '\nГотово: {{ cookiecutter.project_slug }}\n\n'
    '  cd {{ cookiecutter.project_slug }}\n'
    '  git init\n'
    '  make install requirements   # poetry install + requirements.txt для Docker\n'
    '  make infra-up migrate run   # инфраструктура, миграции, API на :8000\n'
)
