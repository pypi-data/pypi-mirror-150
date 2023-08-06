import logging
from rich.logging import RichHandler
import sys


def get_logger():
    logger = logging.getLogger('audit_tools')
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler('audit_tools.log', mode='w')
    file_handler.setLevel(logging.DEBUG)

    rich_handler = RichHandler(rich_tracebacks=True)

    #stream_handler = logging.StreamHandler(stream=sys.stdout)
    #stream_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | (%(filename)s:%(lineno)s via %(funcName)s) | %(message)s\n',
        datefmt='%Y-%m-%d | %H:%M:%S'
    )

    file_handler.setFormatter(formatter)
    #stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(rich_handler)

    return logger
