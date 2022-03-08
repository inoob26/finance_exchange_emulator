from typing import Optional


def get_logger(log_level: str, log_file: Optional[str] = None) -> dict:
    config = {
        "version": 1,
        "formatters": {
            "json": {
                "class": "common_logging.formatters.JSONFormatter",
            },
            'default': {
                'format': '%(levelname)s %(asctime)s.%(msecs)04d %(module)s %(filename)s:%(lineno)d %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "json",
                "stream": "ext://sys.stdout"
            }
        },
        'loggers': {
            '': {'level': log_level, 'handlers': ['console']},
        },
    }

    if log_file:
        config['handlers']['file'] = {
            'class': 'logging.FileHandler',
            'filename': str(log_file),
            'level': log_level,
            'mode': 'a',
            'formatter': 'default',
        }
        for cfg in config['loggers'].values():
            cfg['handlers'].append('file')
    return config
