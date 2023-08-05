import os
from logging import getLogger, StreamHandler, Formatter, getLevelName

__LOG_FORMAT = os.getenv("LOG_FORMAT", "[%(levelname)s] [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s")
__LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

LEVEL_NAME = getLevelName(__LOG_LEVEL)

HANDLER = StreamHandler()
HANDLER.setLevel(LEVEL_NAME)
HANDLER.setFormatter(Formatter(__LOG_FORMAT))


def set_logger(cls: type):
    log = getLogger(cls.__name__)
    log.setLevel(LEVEL_NAME)
    log.addHandler(HANDLER)
    log.propagate = False
    cls.log = log
    return cls
