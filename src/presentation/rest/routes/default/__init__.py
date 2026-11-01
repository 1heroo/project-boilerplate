from fastapi import APIRouter

from src.presentation.rest.routes.default.health_check import router as health_check_router


def bind_default_routes() -> APIRouter:
    router = APIRouter()
    router.include_router(health_check_router)
    return router
