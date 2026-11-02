"""Bounded, finite JSON input shared by exported data and geometry."""

import hashlib
import json
import math

from .streams import read_bounded

MAX_DATA_BYTES = 64 * 1024 * 1024


class DataError(ValueError):
    """Invalid external game data, with source context."""


def read_json(path, *, expected_sha256=None):
    def invalid_constant(value):
        raise ValueError(f"non-finite number {value}")

    def finite_float(value):
        number = float(value)
        if not math.isfinite(number):
            invalid_constant(value)
        return number

    try:
        with path.open("rb") as stream:
            payload = read_bounded(stream, MAX_DATA_BYTES)
        if len(payload) > MAX_DATA_BYTES:
            raise ValueError("exceeds the 64 MiB data limit")
        if (
            expected_sha256 is not None
            and hashlib.sha256(payload).hexdigest().lower() != expected_sha256.lower()
        ):
            raise ValueError(
                "manifest hash mismatch; export is incomplete or has changed"
            )
        return json.loads(
            payload.decode("utf-8"),
            parse_constant=invalid_constant,
            parse_float=finite_float,
        )
    except (ValueError, UnicodeError) as error:
        raise DataError(f"Invalid game data {path}: {error}") from error
