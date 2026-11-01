from dishka import AsyncContainer, Provider, make_async_container

from src.infrastructure.di.providers.application.message_bus import MessageBusProvider
from src.infrastructure.di.providers.application.services import ServiceProvider
from src.infrastructure.di.providers.persistence.db import DBProvider
from src.infrastructure.di.providers.persistence.repositories import RepositoryProvider
from src.infrastructure.di.providers.tasks import TasksProvider


def default_providers() -> list[Provider]:
    return [
        DBProvider(),
        RepositoryProvider(),
        ServiceProvider(),
        MessageBusProvider(),
        TasksProvider(),
    ]


def get_async_container() -> AsyncContainer:
    return make_async_container(*default_providers())
