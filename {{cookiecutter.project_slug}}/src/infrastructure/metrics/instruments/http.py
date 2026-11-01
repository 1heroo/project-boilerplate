import src.infrastructure.metrics.multiprocess  # noqa: F401

from prometheus_client import Counter, Histogram

UNMATCHED_ENDPOINT = 'unmatched'

HTTP_REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint'],
)
HTTP_REQUESTS = Counter(
    'http_request_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'http_status'],
)


def observe_request(method: str, endpoint: str | None, status_code: int, elapsed: float) -> None:
    endpoint = endpoint or UNMATCHED_ENDPOINT
    HTTP_REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(elapsed)
    HTTP_REQUESTS.labels(method=method, endpoint=endpoint, http_status=str(status_code)).inc()
