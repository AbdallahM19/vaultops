"""Logging Module"""

import logging


formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
)
console = logging.StreamHandler()

console.setFormatter(formatter)

logger = logging.getLogger("vaultops")
logger.addHandler(console)

def setup_logging(
        level: int = logging.INFO
) -> logging.Logger:
    logger.setLevel(level)
    return logger
