from src.domain.exceptions.codes import CoreErrorCodesEnum
from src.domain.exceptions.core import CoreException


class ItemNotFoundException(CoreException):
    def __init__(self, item_id: int):
        super().__init__(CoreErrorCodesEnum.NO_DATA_FOUND, f'Элемент {item_id} не найден.')


class ItemAlreadyExistsException(CoreException):
    def __init__(self, title: str):
        super().__init__(
            CoreErrorCodesEnum.DATA_ALREADY_EXISTS,
            f'Элемент с названием {title!r} уже существует.',
        )
