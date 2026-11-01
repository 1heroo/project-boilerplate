"""Dedicated app serving Prometheus metrics.

Every process of the service writes samples to PROMETHEUS_MULTIPROC_DIR; this
process aggregates them and serves /metrics. State that lives outside the
processes is added as a `ScrapeSource` (see infrastructure/metrics/collectors).
"""
from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST

from src.config.logger.config import setup_logging
from src.config.settings import settings
from src.infrastructure.metrics.collectors.base import ScrapeSource
from src.infrastructure.metrics.scrape import Scraper


def scrape_sources() -> list[ScrapeSource]:
    return []


def create_app() -> FastAPI:
    setup_logging()
    scraper = Scraper(scrape_sources(), timeout=settings.prometheus.scrape_timeout_seconds)
    app = FastAPI(title=f'{settings.fastapi.title} metrics', docs_url=None, redoc_url=None, openapi_url=None)

    @app.get('/health/check', include_in_schema=False)
    async def health() -> dict[str, str]:
        return {'status': 'ok'}

    @app.get('/metrics', include_in_schema=False)
    async def metrics() -> Response:
        return Response(content=await scraper.render(), media_type=CONTENT_TYPE_LATEST)

    return app


app = create_app()
