import logging
from typing import Optional

from audit_tools.core.session import Session

log = logging.getLogger('audit_tools')


class SessionManager:
    def __init__(self, file_path: Optional[str] = None, folder_path: Optional[str] = None, testing: bool = False):
        self.file_path = file_path
        self.folder_path = folder_path
        self.session = None
        self.testing = testing
        if testing:
            log.warning("SessionManager initialized in testing mode")

    def __enter__(self) -> Session:

        if self.file_path:
            self.session = Session(self.file_path)
        else:
            self.session = Session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session.products.empty:
            log.error("No products found in session")
        else:
            if not self.testing:
                log.info("Exiting and saving session to disk")
                self.session.shutdown(self.folder_path)
