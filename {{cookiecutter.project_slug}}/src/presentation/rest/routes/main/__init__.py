from fastapi import APIRouter
{%- if cookiecutter.include_example %}

from src.presentation.rest.routes.main.items.routes import router as items_router
{%- endif %}

API_V1_PREFIX = '/api/v1'


def bind_main_routes() -> APIRouter:
    router = APIRouter(prefix=API_V1_PREFIX)
{%- if cookiecutter.include_example %}
    router.include_router(items_router)
{%- endif %}
    return router
