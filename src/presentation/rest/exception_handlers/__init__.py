from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from src.domain.enums.rest.handler import ExceptionHandlerEnum
from src.domain.exceptions import CoreException
from src.presentation.rest.exception_handlers.domain import handle_domain_exception
from src.presentation.rest.exception_handlers.system import handle_system_exception
from src.presentation.rest.exception_handlers.validation import handle_validation_error


def register_exception_handlers(
    app: FastAPI, handlers: list[ExceptionHandlerEnum] | None = None,
) -> None:
    for handler in handlers or list(ExceptionHandlerEnum):
        match handler:
            case ExceptionHandlerEnum.SYSTEM:
                app.add_exception_handler(Exception, handle_system_exception)
            case ExceptionHandlerEnum.VALIDATION:
                app.add_exception_handler(RequestValidationError, handle_validation_error)
                app.add_exception_handler(ValidationError, handle_validation_error)
            case ExceptionHandlerEnum.DOMAIN:
                app.add_exception_handler(CoreException, handle_domain_exception)
