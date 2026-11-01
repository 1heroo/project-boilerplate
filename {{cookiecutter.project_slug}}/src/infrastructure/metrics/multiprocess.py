"""Prometheus multiprocess mode for every process of the service.

`prometheus_client` picks its value storage on first import, so this module must
be imported before it: every instruments module does that first.
"""
import os
from pathlib import Path

from src.config.settings import settings

BASE_DIR = Path(__file__).resolve().parents[3]
mp_dir = str(BASE_DIR / settings.prometheus.multiproc_dir)

os.environ.setdefault('PROMETHEUS_MULTIPROC_DIR', mp_dir)
os.makedirs(os.environ['PROMETHEUS_MULTIPROC_DIR'], exist_ok=True)
