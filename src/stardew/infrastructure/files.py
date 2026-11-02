"""Validate destinations and atomically replace files in their own directories."""

from __future__ import annotations

import os
import tempfile
from collections.abc import Iterable, Mapping
from pathlib import Path


def atomic_write(path: str | Path, data: bytes) -> Path:
    destination = Path(path)
    atomic_write_many({destination: data})
    return destination


def atomic_write_many(files: Mapping[Path, bytes]) -> None:
    """Stage every payload before replacing any destination.

    Each replacement is atomic, but a crash during replacement can publish only
    part of a batch. Multi-file formats must use a verified manifest.
    """
    for path in files:
        validate_destination(path)
    atomic_write_stream(files.items())


def validate_destination(path: Path) -> None:
    if path.is_symlink():
        raise ValueError(f"Refusing to overwrite a symbolic link: {path}")
    if path.exists() and not path.is_file():
        raise ValueError(f"Output destination is not a file: {path}")


def atomic_write_stream(files: Iterable[tuple[Path, bytes]]) -> None:
    """Stage lazily produced payloads; publish only after every producer succeeds."""
    staged = []
    destinations = set()
    try:
        for path, data in files:
            if path in destinations:
                raise ValueError(f"Duplicate output destination: {path}")
            destinations.add(path)
            validate_destination(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            descriptor, temporary_name = tempfile.mkstemp(
                prefix=f".{path.name}.", dir=path.parent
            )
            staged.append((path, Path(temporary_name)))
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
        for path, temporary in staged:
            validate_destination(path)
            os.replace(temporary, path)
    finally:
        for _, temporary in staged:
            temporary.unlink(missing_ok=True)
