from typing import Any

from taskiq import TaskiqMessage, TaskiqMiddleware, TaskiqResult

from src.config.logger.context import NO_TRACE, accept_trace_id, bind, get_trace_id, new_trace_id, unbind

TRACE_LABEL = 'trace_id'


class LogContextMiddleware(TaskiqMiddleware):
    """Carry the trace id from whoever enqueued a task into the worker's logs."""

    def pre_send(self, message: TaskiqMessage) -> TaskiqMessage:
        if TRACE_LABEL not in message.labels:
            current = get_trace_id()
            message.labels[TRACE_LABEL] = current if current != NO_TRACE else new_trace_id()
        return message

    def pre_execute(self, message: TaskiqMessage) -> TaskiqMessage:
        bind(
            accept_trace_id(str(message.labels.get(TRACE_LABEL) or '')),
            task_name=message.task_name,
            task_id=message.task_id,
        )
        return message

    def post_execute(self, message: TaskiqMessage, result: TaskiqResult[Any]) -> None:
        unbind()
