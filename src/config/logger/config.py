import json
import logging.config
from pathlib import Path

from src.config.settings import settings

LOGGING_CONFIG_PATH = Path(__file__).resolve().parent / 'logging.json'


def setup_logging() -> None:
    """`logging.json` (also given to uvicorn as `--log-config`) with format and level from config."""
    config = json.loads(LOGGING_CONFIG_PATH.read_text())
    config['handlers']['console']['formatter'] = settings.logging.format
    config['root']['level'] = settings.logging.level.upper()
    logging.config.dictConfig(config)
