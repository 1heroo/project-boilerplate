import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.domain.exceptions import CoreErrorCodesEnum, CoreException

logger = logging.getLogger(__name__)

CODE_TO_HTTP_STATUS: dict[int, int] = {
    CoreErrorCodesEnum.NO_DATA_FOUND: status.HTTP_404_NOT_FOUND,
    CoreErrorCodesEnum.NOT_AUTHORIZED: status.HTTP_401_UNAUTHORIZED,
    CoreErrorCodesEnum.INVALID_AUTH: status.HTTP_401_UNAUTHORIZED,
    CoreErrorCodesEnum.PERMISSION_DENIED: status.HTTP_403_FORBIDDEN,
    CoreErrorCodesEnum.DATA_ALREADY_EXISTS: status.HTTP_409_CONFLICT,
    CoreErrorCodesEnum.DATA_VALIDATION_ERROR: status.HTTP_422_UNPROCESSABLE_ENTITY,
    CoreErrorCodesEnum.SERVICE_UNAVAILABLE: status.HTTP_503_SERVICE_UNAVAILABLE,
    CoreErrorCodesEnum.SYSTEM_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
}


async def handle_domain_exception(request: Request, exc: CoreException) -> JSONResponse:
    status_code = CODE_TO_HTTP_STATUS.get(exc.code, status.HTTP_400_BAD_REQUEST)
    logger.log(
        logging.ERROR if status_code >= 500 else logging.WARNING,
        'Ошибка %s: %s', exc.code, exc.message,
        extra={'error_code': exc.code, 'http_status': status_code},
        exc_info=status_code >= 500,
    )
    return JSONResponse(content={'code': exc.code, 'message': exc.message}, status_code=status_code)
