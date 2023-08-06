# from typing import IO, Optional

from ..base import FileStream
from .out import OutStream


class OutFileStream(FileStream, OutStream):
    """
    Class that all out streams that write to files inherit from.
    """

    _default_mode = "w"
