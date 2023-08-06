from sys import stdout

from .out import OutStream


class _Cout(OutStream):
    """
    Class that represents the cout stream.
    Not intended to be used directly, please use the :const:`cppstream.cout` variable instead.
    """

    _stream = stdout
