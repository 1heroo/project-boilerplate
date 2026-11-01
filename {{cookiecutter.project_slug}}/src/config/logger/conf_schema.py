from typing import Literal

from pydantic import BaseModel


class LoggingConfig(BaseModel):
    """Logs go to stdout only; the platform collects them. `plain` is for reading locally."""

    format: Literal['json', 'plain'] = 'json'
    level: str = 'INFO'
