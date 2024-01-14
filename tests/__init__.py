from typing import TextIO


def clear_stream(stream: TextIO):
    """Clears the contents of a given stream

    Args:
        stream (TextIO): The stream to clear.
    """
    if stream.seekable():
        stream.seek(0)
        stream.truncate(0)
