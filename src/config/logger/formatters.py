"""One-line JSON records with secrets masked."""
from typing import Any

from pythonjsonlogger.json import JsonFormatter

MASK = '***'
SENSITIVE_KEYS = frozenset({
    'authorization', 'proxy-authorization', 'cookie', 'set-cookie', 'password', 'passwd',
    'secret', 'token', 'access_token', 'refresh_token', 'api_key', 'apikey', 'api_token',
    'client_secret', 'private_key',
})


def redact(value: Any) -> Any:
    """Mask values under sensitive keys at any depth, case-insensitively."""
    if isinstance(value, dict):
        return {
            key: MASK if str(key).lower() in SENSITIVE_KEYS else redact(item)
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [redact(item) for item in value]
    return value


class RedactingJsonFormatter(JsonFormatter):
    def process_log_record(self, log_data: dict[str, Any]) -> dict[str, Any]:
        return redact(super().process_log_record(log_data))
