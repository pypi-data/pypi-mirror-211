import logging

logging.basicConfig(
    level=logging.INFO, format='{"app_name": "seleniumbot", "time":"%(asctime)s", "name": "%(name)s", '
                               '"level": "%(levelname)s", "msg": "%(message)s"}',
    datefmt="%Y-%m-%dT%H:%M:%S",
)


def get_logger(name: str):
    return logging.getLogger(name)
