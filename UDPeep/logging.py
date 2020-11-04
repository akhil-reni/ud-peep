# -*- coding: utf-8 -*-

import logging
from logging.config import dictConfig


def get_logger() -> logging.Logger:
    dictConfig({
        'version': 1,
        'formatters': {
            'default': {'format': '%(asctime)s - %(levelname)s - %(message)s',
                        'datefmt': '%Y-%m-%d %H:%M:%S'}
        },
        'handlers': {
            'dev': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },

        },
        'loggers': {
            'default': {
                'level': 'DEBUG',
                'handlers': ['dev', ]
            }
        },
        'disable_existing_loggers': False
    })
    return logging.getLogger('default')
