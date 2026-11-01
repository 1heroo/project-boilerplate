"""One `/metrics` response: multiprocess samples plus the scrape-time sources."""
import asyncio
import logging
import time
from collections.abc import Iterable, Iterator, Sequence
from datetime import UTC, datetime

import src.infrastructure.metrics.multiprocess  # noqa: F401

from prometheus_client import CollectorRegistry, generate_latest, multiprocess
from prometheus_client.core import GaugeMetricFamily
from prometheus_client.metrics_core import Metric
from prometheus_client.registry import Collector

from src.infrastructure.metrics.collectors.base import ScrapeSource

logger = logging.getLogger(__name__)


class _Snapshot(Collector):
    def __init__(self, families: Iterable[Metric]):
        self._families = list(families)

    def collect(self) -> Iterator[Metric]:
        yield from self._families


class Scraper:
    """Reads every source concurrently, each bounded by `timeout`."""

    def __init__(self, sources: Sequence[ScrapeSource], timeout: float):
        self._sources = sources
        self._timeout = timeout

    async def render(self) -> bytes:
        now = datetime.now(UTC)
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)
        families: list[Metric] = []
        for read in await asyncio.gather(*(self._read(source, now) for source in self._sources)):
            families.extend(read)
        registry.register(_Snapshot(families))
        return generate_latest(registry)

    async def _read(self, source: ScrapeSource, now: datetime) -> list[Metric]:
        started = time.perf_counter()
        up = GaugeMetricFamily(source.up_name, source.up_help)
        try:
            families = list(await asyncio.wait_for(source.read(now), self._timeout))
        except Exception:  # noqa: BLE001
            logger.exception('Не удалось прочитать %s для метрик', source.up_name)
            up.add_metric([], 0)
            return [up]
        up.add_metric([], 1)
        duration = GaugeMetricFamily(f'{source.up_name}_read_seconds', 'Time to read the source')
        duration.add_metric([], time.perf_counter() - started)
        return [up, duration, *families]
