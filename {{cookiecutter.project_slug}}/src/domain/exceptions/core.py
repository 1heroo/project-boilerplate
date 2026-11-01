from src.domain.exceptions.codes import CoreErrorMessages


class CoreException(Exception):
    """Base of every business error. The central handler maps `code` to an HTTP status."""

    def __init__(self, code: int, message: str | None = None):
        self.code = int(code)
        self.message = str(message) if message else CoreErrorMessages.get_message(self.code)
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'CoreException {self.code}: {self.message}'
