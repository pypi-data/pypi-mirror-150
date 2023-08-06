from .out import OutStream


class _Endl:
    """
    Class that represents the endl character.
    Not intended to be used directly, please use the :data:`cppstream.endl` variable instead.
    When used as a stream operator, this class will write a newline to the stream
    and flush the stream.

    C++ equivalent: none
    """

    _iostream_streamable_from = True

    def __init__(self) -> None:
        pass

    def _iostream_stream_from(self, ostream: OutStream) -> None:
        ostream.stream.flush()
        ostream << ostream.linesep
