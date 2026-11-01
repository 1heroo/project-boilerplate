from enum import Enum


class ExceptionHandlerEnum(str, Enum):
    VALIDATION = 'VALIDATION'
    SYSTEM = 'SYSTEM'
    DOMAIN = 'DOMAIN'
