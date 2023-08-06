import os

from audit_tools.core.utils.file_manager import import_file, export_file
from audit_tools.core.utils.logger import get_logger


def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')
