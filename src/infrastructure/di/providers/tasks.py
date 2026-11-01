from dishka import Provider, Scope, provide

from src.domain.interfaces.tasks import ITaskQueue
from src.infrastructure.tasks.queue import TaskiqTaskQueue


class TasksProvider(Provider):
    task_queue = provide(TaskiqTaskQueue, provides=ITaskQueue, scope=Scope.APP)
