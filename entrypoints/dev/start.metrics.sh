#!/bin/sh
exec uvicorn src.metrics:app --host 0.0.0.0 --port 8002 --log-config /app/src/config/logger/logging.json
