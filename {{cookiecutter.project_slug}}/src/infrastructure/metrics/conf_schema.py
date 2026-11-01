from pydantic import BaseModel


class PrometheusConfig(BaseModel):
    """`multiproc_dir` is shared by every process; the metrics app aggregates it."""

    multiproc_dir: str = 'prometheus_metrics'
    scrape_timeout_seconds: float = 5.0
