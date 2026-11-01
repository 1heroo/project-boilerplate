from abc import ABC, abstractmethod
from collections.abc import Iterable
from datetime import datetime

from prometheus_client.metrics_core import Metric


class ScrapeSource(ABC):
    """External state read on every scrape (queue length from Postgres, consumer lag...).

    The scraper adds `<up_name>` = 1 when the read succeeded and 0 when it failed
    or timed out; a failed source exports nothing else.
    """

    up_name: str
    up_help: str

    @abstractmethod
    async def read(self, now: datetime) -> Iterable[Metric]:
        raise NotImplementedError
