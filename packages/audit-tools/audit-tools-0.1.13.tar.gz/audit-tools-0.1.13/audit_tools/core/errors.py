import logging

logger = logging.getLogger('audit_tools')


class SessionException(Exception):
    """
    SessionException
    """
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        # logger.exception(message)
