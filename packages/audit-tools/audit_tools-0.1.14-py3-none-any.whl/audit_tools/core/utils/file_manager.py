import logging
import os
from typing import Optional

import pandas as pd
import datetime

from audit_tools.core.errors import SessionException

log = logging.getLogger('audit_tools')


def export_file(file_type: str, folder_path: Optional[str], file: pd.DataFrame, testing: bool = False) -> Optional[str]:
    """
    Export a file to the current or specified directory.
    """

    date_time = datetime.datetime.now().strftime("%Y-%m-%d")
    file_name = f"audit-{date_time}.{file_type}"

    if folder_path:
        log.info(f'finding {folder_path}')
        if os.path.isdir(folder_path):
            log.info(f'{folder_path} found')
            file_name = os.path.join(folder_path, file_name)
        else:
            raise SessionException("Invalid file path!")

    if not testing:
        log.info(f"Exporting file to {file_name}")

        log.info(f"Checking file_type and exporting accordingly...")

        if file_type == "csv":
            file.to_csv(file_name, index=False, header=True)

        elif file_type == "xlsx":
            file.to_excel(file_name, index=False, header=True)

        elif file_type == "json":
            file.to_json(file_name, orient="records")

        else:
            raise SessionException("Invalid file type!")

        log.info(f"File exported to {file_name}")
        return file_name
    else:
        log.warning(f"Testing: true - not exporting file to {file_name}")
        return file_name


def import_file(file_path: str) -> [pd.DataFrame, str]:
    """
    Import a file from the current directory.
    """

    _, file_type = file_path.split(".")

    log.info(f"Importing file from {file_path}")

    if file_type == "csv":
        file = pd.read_csv(file_path)
    elif file_type == "xlsx":
        file = pd.read_excel(file_path)
    elif file_type == "json":
        file = pd.read_json(file_path)
    else:
        raise SessionException(f"Invalid file type! {file_type}")

    log.info(f"Setting file_type to {file_type}")

    log.info(f"File imported from {file_path}")

    return file, file_type
