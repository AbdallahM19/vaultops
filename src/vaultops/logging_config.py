"""Logging Module"""

import logging


def setup_logging(
    level: int = logging.INFO
) -> logging.Logger:
    logger = logging.getLogger("vaultops")
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )


    exists = False

    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            exists = True
            break

    if not exists:
        console = logging.StreamHandler()
        console.setFormatter(formatter)

        logger.addHandler(console)

    return logger
