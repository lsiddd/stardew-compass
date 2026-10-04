"""Atomic output and input-save protection shared by every text/JSON command."""

from pathlib import Path
import os
from .loader import SaveError
from stardew.infrastructure.files import atomic_write as atomic_write_bytes


def check_output_path(output, save_path):
    path, save_path = Path(output).expanduser().absolute(), Path(save_path)
    if path.resolve() == save_path.resolve() or (
        path.exists() and os.path.samefile(path, save_path)
    ):
        raise SaveError("Output must not overwrite the input save.")
    if path.is_symlink():
        raise SaveError("Output path must not be a symbolic link.")
    return path


def atomic_write(path, content):
    atomic_write_bytes(path, content.encode("utf-8"))
