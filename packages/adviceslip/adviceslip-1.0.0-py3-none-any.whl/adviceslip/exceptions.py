from enum import Enum
from typing import Optional


class MessageType(Enum):
    """Types for API error messages"""

    NOTICE = "notice"
    WARNING = "warning"
    ERROR = "error"


class SessionClosed(Exception):
    """Raised when the client is closed"""


class HTTPException(Exception):
    """Raised when encountering an HTTP error"""

    def __init__(self, message: str, status_code: int) -> None:
        super().__init__(message)
        self.status_code = status_code


class APIError(Exception):
    """Raised when the API returns an error message"""

    def __init__(self, message: str, *, type: Optional[MessageType] = MessageType.NOTICE) -> None:
        super().__init__(message)
        self.type = type
