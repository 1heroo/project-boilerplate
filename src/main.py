from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.config.logger.config import setup_logging
from src.config.settings import settings
from src.infrastructure.di.ioc_container import get_async_container
from src.infrastructure.persistence.db.models.mapping import run_mappers
from src.presentation.rest.exception_handlers import register_exception_handlers
from src.presentation.rest.middlewares import register_middlewares
from src.presentation.rest.middlewares.forwarded_prefix import ForwardedPrefixMiddleware
from src.presentation.rest.routes.default import bind_default_routes
from src.presentation.rest.routes.main import bind_main_routes


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    setup_logging()
    run_mappers()

    docs = settings.fastapi.docs_enabled
    app = FastAPI(
        title=settings.fastapi.title,
        debug=settings.fastapi.debug,
        lifespan=lifespan,
        docs_url='/docs' if docs else None,
        redoc_url='/redoc' if docs else None,
        openapi_url='/openapi.json' if docs else None,
    )
    register_exception_handlers(app)
    register_middlewares(app)
    app.add_middleware(
        CORSMiddleware,  # noqa
        allow_origins=settings.fastapi.cors_origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app.add_middleware(ForwardedPrefixMiddleware)  # noqa

    app.include_router(bind_default_routes())
    app.include_router(bind_main_routes())

    setup_dishka(get_async_container(), app)
    return app


app = create_app()
