import sys

from loguru import logger

logger.add(
    sys.stdout,
    format="{time} {level} {message}",
    level='DEBUG',
    enqueue=True,
    colorize=True,
    diagnose=False,
)
