from enum import Enum


class CoreErrorCodesEnum(int, Enum):
    SYSTEM_ERROR = -1
    CUSTOM_ERROR = -2
    NO_DATA_FOUND = -3
    NOT_AUTHORIZED = -4
    DATA_ALREADY_EXISTS = -5
    SERVICE_UNAVAILABLE = -6
    DATA_VALIDATION_ERROR = -7
    INVALID_AUTH = -8
    PERMISSION_DENIED = -15


class CoreErrorMessages:
    _messages: dict[int, str] = {
        CoreErrorCodesEnum.SYSTEM_ERROR: 'Системная ошибка, пожалуйста, попробуйте позже!',
        CoreErrorCodesEnum.CUSTOM_ERROR: '',
        CoreErrorCodesEnum.NO_DATA_FOUND: 'Данные не найдены!',
        CoreErrorCodesEnum.NOT_AUTHORIZED: 'Вы не авторизованы, пожалуйста, войдите в систему!',
        CoreErrorCodesEnum.DATA_ALREADY_EXISTS: 'Данные уже существуют!',
        CoreErrorCodesEnum.SERVICE_UNAVAILABLE: 'Сервис недоступен!',
        CoreErrorCodesEnum.DATA_VALIDATION_ERROR: 'Ошибка проверки данных!',
        CoreErrorCodesEnum.INVALID_AUTH: 'Некорректный логин или пароль!',
        CoreErrorCodesEnum.PERMISSION_DENIED: 'Нет доступа к этому функционалу.',
    }

    @classmethod
    def get_message(cls, code: int) -> str:
        return cls._messages.get(code, cls._messages[CoreErrorCodesEnum.SYSTEM_ERROR])
