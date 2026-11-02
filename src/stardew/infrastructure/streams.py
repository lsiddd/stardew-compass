"""Bounded input without allocating the maximum allowed size for small files."""

from io import BytesIO
from typing import BinaryIO


def read_bounded(stream: BinaryIO, limit: int) -> bytes:
    """Read at most limit + 1 bytes so the caller can diagnose oversized input."""
    with BytesIO() as output:
        remaining = limit + 1
        while remaining:
            chunk = stream.read(min(1024 * 1024, remaining))
            if not chunk:
                break
            output.write(chunk)
            remaining -= len(chunk)
        return output.getvalue()
