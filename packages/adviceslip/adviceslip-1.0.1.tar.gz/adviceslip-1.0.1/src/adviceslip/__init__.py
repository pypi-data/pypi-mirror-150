from sys import version_info

if version_info < (3, 8):
    raise RuntimeError("Python 3.8 or higher is required to use this library")

del version_info

from typing import NamedTuple

from .client import Client
from .exceptions import APIError, HTTPException, SessionClosed
from .objects import Search, Slip


class VersionInfo(NamedTuple):
    """Version information for the library

    Args:
        major (int): The major version number
        minor (int): The minor version number
        micro (int): The micro version number
    """

    major: int
    minor: int
    micro: int


__version__ = VersionInfo(major=1, minor=0, micro=1)

del VersionInfo, NamedTuple
