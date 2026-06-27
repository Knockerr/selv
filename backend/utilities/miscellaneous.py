import sys
from loguru import logger


def initLogger():
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{file.name}</cyan> | "
               "{message}",
        colorize=True)

