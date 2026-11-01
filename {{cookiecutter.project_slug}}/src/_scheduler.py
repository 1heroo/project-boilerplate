"""Taskiq scheduler entry point: `taskiq scheduler src._scheduler:scheduler`.

Only enqueues scheduled jobs; the worker executes them. Run exactly one instance.
"""
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource

import src.infrastructure.tasks.jobs  # noqa: F401
from src.config.logger.config import setup_logging
from src.infrastructure.tasks.broker import task_broker

setup_logging()

scheduler = TaskiqScheduler(broker=task_broker, sources=[LabelScheduleSource(task_broker)])
