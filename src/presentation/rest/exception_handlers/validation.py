import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.domain.exceptions.codes import CoreErrorCodesEnum

logger = logging.getLogger(__name__)


def _location(loc: tuple[int | str, ...]) -> str:
    parts = loc[1:] if loc and loc[0] == 'body' else loc
    return '.'.join(str(part) for part in parts)


async def handle_validation_error(
    request: Request, exc: RequestValidationError | ValidationError,
) -> JSONResponse:
    """Logs where and why validation failed, never the submitted values."""
    errors = exc.errors()
    logger.warning(
        'Невалидный запрос: %s',
        '; '.join(f"{_location(item['loc'])}: {item['msg']}" for item in errors),
    )
    first = errors[0]
    return JSONResponse(
        content={
            'code': CoreErrorCodesEnum.DATA_VALIDATION_ERROR,
            'message': f"{_location(first['loc'])}: {first['msg']}",
        },
        status_code=400,
    )
