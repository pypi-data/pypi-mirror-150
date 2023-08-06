from __future__ import annotations

from os import linesep
from pathlib import Path
from typing import IO, AnyStr, Optional

PathLike = Path | str | bytes


class Stream:
    """
    Base class that all stream objects inherit from. This class is not meant to be used directly.
    C++ equivalent: ``std::basic_ios<char>``
    """

    _linesep: AnyStr = linesep
    _stream: IO

    def __init__(self) -> None:
        pass

    @property
    def linesep(self) -> str:
        """
        The line separator for this stream. Defaults to :data:`os.linesep`.
        C++ equivalent: none
        """

        return self._linesep

    @property
    def stream(self) -> IO:
        """
        The raw file object for this stream.
        C++ equivalent: ``std::basic_ios<char>::rdbuf()``
        """

        return self._stream


class FileStream(Stream):
    """
    Base class that all stream objects that write to files inherit from.
    This class is not meant to be used directly.
    C++ equivalent: ``std::basic_fstream<char>``

    :param path: The path to the file to open.
    :type path: Optional[PathLike]
    :param mode: The mode to open the file in, defaults to :attr:`default_mode`.
    :type mode: Optional[str]
    """

    _linesep = "\n"
    _is_open: bool = False
    _default_mode = "r"

    def __init__(
        self, path: Optional[PathLike] = None, mode: Optional[str] = None
    ) -> None:
        if path is not None:
            self.open(path, mode)

    def __enter__(self) -> FileStream:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def open(self, path: str, mode: Optional[str] = None) -> None:
        """
        Open the stream from ``path`` for reading or writing.
        C++ equivalent: ``std::basic_fstream<char>::open``
        """

        self._stream = open(path, mode=mode or self.default_mode)
        self._is_open = True

    def close(self) -> None:
        """
        Close the connected file object, after flushing it. Sets :attr:`is_open` to False.
        C++ equivalent: ``std::basic_fstream<char>::close()``
        """

        self._is_open = False
        self.stream.flush()
        self.stream.close()

    @property
    def is_open(self) -> bool:
        """
        True if the file is open, False otherwise.
        C++ equivalent: ``std::basic_fstream<char>::is_open()``
        """

        return self._is_open

    @property
    def default_mode(self) -> str:
        """
        The default mode to open the file in when opening it.
        C++ equivalent: none
        """

        return self._default_mode
