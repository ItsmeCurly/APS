import logging
import sys

from loguru import logger

from aps.conf import settings


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2

        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def configure_logging():
    logger.remove()

    logger.add(sys.stderr, level=settings.LOG_LEVEL)
    logger.add("main.log", rotation="50 MB", level=settings.LOG_LEVEL)

    if settings.LOG_LEVEL <= logging.DEBUG:
        logger.add("debug.log", rotation="50 MB", level=logging.DEBUG)

    logger.add("benchmark.log", filter=lambda record: "benchmark" in record["extra"])

    logging.basicConfig(handlers=[InterceptHandler()], level=settings.LOG_LEVEL)

    logger.info("Begin Session")


def log_metrics(s: str):
    logger.bind(benchmark=True).info(s)
