import logging
import pathlib
from logging.config import fileConfig

fileConfig(f"{pathlib.Path(__file__).parent}/log.ini")


def getLogger(name, level="INFO"):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger


if __name__ == "__main__":
    logger = getLogger("TEST")
    logger.info("INFO")
    logger.debug("DEBUG")

