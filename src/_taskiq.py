"""Taskiq worker entry point: `taskiq worker src._taskiq:broker`."""
from dishka.integrations.taskiq import setup_dishka
from taskiq import TaskiqEvents, TaskiqState

import src.infrastructure.tasks.jobs  # noqa: F401
from src.config.logger.config import setup_logging
from src.config.settings import settings
from src.infrastructure.di.ioc_container import get_async_container
from src.infrastructure.persistence.db.models.mapping import run_mappers
from src.infrastructure.tasks.broker import task_broker
from src.infrastructure.tasks.health_server import start_health_server

setup_logging()
run_mappers()
setup_dishka(get_async_container(), task_broker)

broker = task_broker


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def start_liveness(state: TaskiqState) -> None:
    state.health_server = await start_health_server('0.0.0.0', settings.taskiq.health_port)


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def stop_liveness(state: TaskiqState) -> None:
    state.health_server.close()
    await state.health_server.wait_closed()
