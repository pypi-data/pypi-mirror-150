import logging
from typing import Optional

from audit_tools.core.session import Session


class SessionManager:
    def __init__(self, file_path: Optional[str] = None, folder_path: Optional[str] = '', testing: bool = False):
        self.file_path = file_path
        self.folder_path = folder_path
        self.session = None
        self.testing = testing

    def __enter__(self) -> Session:

        if self.file_path:
            self.session = Session(self.file_path, testing=self.testing)
        else:
            self.session = Session(testing=self.testing)
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session.products.empty:
            return
        else:
            if not self.testing:
                self.session.shutdown(self.folder_path)
                return
