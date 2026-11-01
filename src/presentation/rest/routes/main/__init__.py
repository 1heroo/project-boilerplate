from fastapi import APIRouter

from src.presentation.rest.routes.main.items.routes import router as items_router

API_V1_PREFIX = '/api/v1'


def bind_main_routes() -> APIRouter:
    router = APIRouter(prefix=API_V1_PREFIX)
    router.include_router(items_router)
    return router
