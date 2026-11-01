from dishka.integrations.faststream import setup_dishka
from faststream.asgi import AsgiFastStream

from src.config.logger.config import setup_logging
from src.config.settings import settings
from src.infrastructure.di.ioc_container import get_async_container
from src.infrastructure.persistence.db.models.mapping import run_mappers
from src.presentation.broker.health import make_health_routes
from src.presentation.broker.router_register import broker as kafka_broker


def create_app() -> AsgiFastStream:
    setup_logging()
    run_mappers()
    app = AsgiFastStream(kafka_broker, asgi_routes=make_health_routes(), title=f'{settings.fastapi.title} broker')
    setup_dishka(container=get_async_container(), app=app, auto_inject=True)
    return app


app = create_app()
