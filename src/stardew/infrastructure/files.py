"""Validate destinations and atomically replace files in their own directories."""

from __future__ import annotations

from collections.abc import Mapping
import os
from pathlib import Path
import tempfile


def atomic_write(path: str | Path, data: bytes) -> Path:
    destination = Path(path)
    atomic_write_many({destination: data})
    return destination


def atomic_write_many(files: Mapping[Path, bytes]) -> None:
    """Stage every payload before replacing any destination.

    Each replacement is atomic. Multiple files are validated and staged together,
    so malformed inputs or unsafe destinations cannot leave partial exports.
    """
    for path in files:
        if path.is_symlink():
            raise ValueError(f"Refusing to overwrite a symbolic link: {path}")
        if path.exists() and not path.is_file():
            raise ValueError(f"Output destination is not a file: {path}")
    staged = []
    try:
        for path, data in files.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            descriptor, temporary = tempfile.mkstemp(
                prefix=f".{path.name}.", dir=path.parent
            )
            staged.append((path, Path(temporary)))
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
        for path, temporary in staged:
            if path.is_symlink():
                raise ValueError(f"Refusing to overwrite a symbolic link: {path}")
            os.replace(temporary, path)
    finally:
        for _, temporary in staged:
            temporary.unlink(missing_ok=True)
