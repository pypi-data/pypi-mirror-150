import logging
from logging.config import dictConfig


class DebugLevelFilter(logging.Filter):

    def filter(self, record):
        return record.levelno == logging.DEBUG


LOGGER_NAME = 'asyncspawner'

LOGGER_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(levelname)s] %(asctime)s - %(name)s - %(message)s',
        },
        'debug': {
            'format': '[%(levelname)s] %(asctime)s %(processName)s:%(threadName)s %(filename)s:%(funcName)s:%(lineno)d - %(name)s - %(message)s',
        },
    },
    'filters': {
        'debug': {
            '()': DebugLevelFilter,
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'default',
            'class': 'logging.StreamHandler',
        },
        'debug': {
            'level': 'DEBUG',
            'formatter': 'debug',
            'class': 'logging.StreamHandler',
            'filters': ['debug']
        },
    },
    'loggers': {
        LOGGER_NAME: {
            'handlers': ['default', 'debug'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


dictConfig(LOGGER_CONFIG)


def get_logger(level='INFO'):
    logger = logging.getLogger(LOGGER_NAME)

    try:
        logger.setLevel(logging.getLevelName(level))
    except ValueError:
        pass

    return logger
