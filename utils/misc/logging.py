import logging
import os
from datetime import datetime

from data.config import DEBUG


def set_logging_level() -> None:
    if DEBUG:
        if not os.path.exists("./logs"):
            os.mkdir("./logs")

        log_formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)-6s] [%(name)s.%(funcName)s:%(lineno)d] %(message)s")
        log_file_handler = logging.FileHandler(f"./logs/bot_logs_{datetime.now().strftime('(%Y-%m-%d)_(%H-%M)')}.txt",
                                               encoding="UTF-8")
        log_file_handler.setFormatter(log_formatter)
        log_console_handler = logging.StreamHandler()
        log_console_handler.setFormatter(log_formatter)

        logging.basicConfig(
            level=logging.DEBUG,
            format="[%(asctime)s] [%(levelname)-6s] [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
            handlers=[log_console_handler, log_file_handler]
        )
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] [%(levelname)-6s] [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
        )
