import atexit
import logging.config
import os
import pathlib

import yaml

logger = logging.getLogger(__name__)


def setup_logging():
    os.makedirs("logs", exist_ok=True)

    config_file = pathlib.Path("./configs/log.dev.yaml")
    with open(config_file) as f_in:
        config = yaml.safe_load(f_in)

    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)
