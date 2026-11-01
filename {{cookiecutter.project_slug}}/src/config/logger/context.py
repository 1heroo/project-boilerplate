"""Log context of the current request, broker message or background task.

Every record gets `trace_id` and the bound fields, so one search by `trace_id`
shows everything a request did, across processes.
"""
import contextvars
import logging
import re
import uuid
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from types import MappingProxyType
from typing import Any

NO_TRACE = '-'
_VALID_TRACE = re.compile(r'^[A-Za-z0-9._:-]{1,128}$')

_TRACE_ID: contextvars.ContextVar[str] = contextvars.ContextVar('trace_id', default=NO_TRACE)
_FIELDS: contextvars.ContextVar[Mapping[str, Any]] = contextvars.ContextVar(
    'log_fields', default=MappingProxyType({}),
)


def new_trace_id() -> str:
    return uuid.uuid4().hex


def accept_trace_id(value: str | None) -> str:
    """A caller's id (`X-Request-ID`, task label) if it is safe to log, otherwise a new one."""
    if value and _VALID_TRACE.match(value):
        return value
    return new_trace_id()


def get_trace_id() -> str:
    return _TRACE_ID.get()


def get_fields() -> Mapping[str, Any]:
    return _FIELDS.get()


@contextmanager
def log_context(trace_id: str | None = None, **fields: Any) -> Iterator[str]:
    """Bind a trace id (kept from the outer context when not given) and fields until exit."""
    trace_token = _TRACE_ID.set(trace_id) if trace_id is not None else None
    fields_token = _FIELDS.set(MappingProxyType({**_FIELDS.get(), **fields}))
    try:
        yield _TRACE_ID.get()
    finally:
        _FIELDS.reset(fields_token)
        if trace_token is not None:
            _TRACE_ID.reset(trace_token)


def bind(trace_id: str, **fields: Any) -> None:
    """Bind for the rest of the current asyncio task, for hooks that cannot wrap the work."""
    _TRACE_ID.set(trace_id)
    _FIELDS.set(MappingProxyType(dict(fields)))


def unbind() -> None:
    _TRACE_ID.set(NO_TRACE)
    _FIELDS.set(MappingProxyType({}))


class ContextFilter(logging.Filter):
    """Copy the context onto the record; fields passed in `extra` win."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = get_trace_id()
        for key, value in get_fields().items():
            if not hasattr(record, key):
                setattr(record, key, value)
        return True
