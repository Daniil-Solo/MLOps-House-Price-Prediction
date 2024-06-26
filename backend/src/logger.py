"""Module for logging."""

import logging
from multiprocessing import Queue

from logging_loki import LokiQueueHandler

from src.config import app_config

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)

loki_logs_handler = LokiQueueHandler(
    Queue(-1),
    url=app_config.LOGGING_URL,
    tags={"application": "fastapi"},
    version="1",
)

uvicorn_logger = logging.getLogger("uvicorn.access")
uvicorn_logger.addHandler(loki_logs_handler)

logger = logging.getLogger(__name__)
logger.addHandler(loki_logs_handler)
