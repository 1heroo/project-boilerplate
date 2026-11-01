"""Taskiq broker shared by the API (enqueue), the worker and the scheduler.

Redis Streams acknowledge a task only after it finishes, so a crashed worker
gets the message redelivered instead of losing it.
"""
from taskiq_redis import RedisStreamBroker

from src.config.settings import settings
from src.infrastructure.tasks.log_context import LogContextMiddleware

task_broker = RedisStreamBroker(url=settings.redis_url).with_middlewares(LogContextMiddleware())
