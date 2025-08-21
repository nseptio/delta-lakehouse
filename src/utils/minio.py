import logging
from functools import lru_cache
from typing import Optional
from urllib.parse import urlparse

from minio import Minio

from .config import Config
from .logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def _parse_url(endpoint: str) -> tuple[str, bool]:
    parsed = urlparse(endpoint)

    if not parsed.scheme:
        return endpoint, False

    if parsed.scheme == "localhost":
        return endpoint, False

    secure = parsed.scheme == "https"
    host = parsed.netloc or parsed.path

    return host, secure


@lru_cache(maxsize=1)
def get_minio_client(config: Optional[Config] = None) -> Minio:
    cfg = config or Config()
    endpoint = cfg.minio_endpoint.encoded_string()
    logger.debug(f"raw endpoint={endpoint}")
    host, secure = _parse_url(endpoint)
    logger.debug(f"parsing minio endpoint host={host} secure={secure}")

    client = Minio(
        endpoint=host,
        access_key=cfg.minio_access_key,
        secret_key=cfg.minio_secret_key,
        secure=secure,
    )

    return client
