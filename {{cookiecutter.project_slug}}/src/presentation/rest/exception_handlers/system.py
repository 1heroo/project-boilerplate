import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from src.config.logger.context import log_context
from src.domain.exceptions.codes import CoreErrorCodesEnum, CoreErrorMessages
from src.presentation.rest.middlewares.logging import TRACE_SCOPE_KEY

logger = logging.getLogger(__name__)


async def handle_system_exception(request: Request, exc: Exception) -> JSONResponse:
    """Runs outside the middlewares, so the trace id is taken back from the ASGI scope."""
    with log_context(request.scope.get(TRACE_SCOPE_KEY)):
        logger.error(
            'Необработанная ошибка: %s %s', request.method, request.url.path,
            exc_info=(type(exc), exc, exc.__traceback__),
        )
    return JSONResponse(
        content={
            'code': CoreErrorCodesEnum.SYSTEM_ERROR,
            'message': CoreErrorMessages.get_message(CoreErrorCodesEnum.SYSTEM_ERROR),
        },
        status_code=500,
    )
