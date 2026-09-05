"""Bounded, read-only save loading and atomic report output."""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import os
import tempfile
import zlib
from lxml import etree

MAX_SAVE_BYTES = 128 * 1024 * 1024


class SaveError(ValueError):
    """Invalid input, reported without an internal traceback by the CLI."""


@dataclass(frozen=True)
class Save:
    path: Path
    tree: etree._ElementTree

    @property
    def root(self):
        return self.tree.getroot()


def resolve_save(value: str | Path) -> Path:
    path = Path(value).expanduser().resolve()
    if path.is_dir():
        path = path / path.name
    if not path.is_file():
        raise SaveError(f"Save file does not exist: {path}")
    return path


def read_save(value: str | Path) -> Save:
    path = resolve_save(value)
    with path.open("rb") as source:
        data = source.read(MAX_SAVE_BYTES + 1)
    if len(data) > MAX_SAVE_BYTES:
        raise SaveError("Save exceeds the 128 MiB input limit.")
    if not data:
        raise SaveError("Save file is empty.")
    prefix = data.lstrip(b"\xef\xbb\xbf \t\r\n")
    if not (prefix.startswith(b"<") or data.startswith((b"\xff\xfe", b"\xfe\xff"))):
        try:
            inflater = zlib.decompressobj()
            data = inflater.decompress(data, MAX_SAVE_BYTES + 1)
            if len(data) > MAX_SAVE_BYTES or inflater.unconsumed_tail:
                raise SaveError("Decompressed save exceeds the 128 MiB limit.")
            if not inflater.eof or inflater.unused_data:
                raise SaveError("Compressed save is truncated or has trailing data.")
        except zlib.error as error:
            raise SaveError(
                "File is neither XML nor a valid zlib-compressed save."
            ) from error
    # A BOM followed by whitespace before the declaration is common in exports.
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    data = data.lstrip(b" \t\r\n")
    parser = etree.XMLParser(resolve_entities=False, load_dtd=False, no_network=True)
    try:
        root = etree.fromstring(data, parser=parser)
    except etree.XMLSyntaxError as error:
        raise SaveError(f"Invalid save XML: {error.msg}") from error
    tree = root.getroottree()
    if tree.docinfo.doctype:
        raise SaveError("Save XML must not contain a DTD.")
    if root.tag != "SaveGame" or root.find("player") is None:
        raise SaveError(
            "Use the full farmer_ID save, not SaveGameInfo (which is only a summary)."
        )
    for field in ("player/name", "uniqueIDForThisGame"):
        if not root.findtext(field):
            raise SaveError(f"Save is missing the required field {field}.")
    return Save(path, tree)


def check_output_path(output: str | Path, save_path: Path) -> Path:
    path = Path(output).expanduser().absolute()
    if path.resolve() == save_path.resolve() or (
        path.exists() and os.path.samefile(path, save_path)
    ):
        raise SaveError("Output must not overwrite the input save.")
    if path.is_symlink():
        raise SaveError("Output path must not be a symbolic link.")
    return path


def atomic_write(path: Path, content: str) -> None:
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            prefix=f".{path.name}.",
            delete=False,
        ) as out:
            temporary = Path(out.name)
            out.write(content)
            out.flush()
            os.fsync(out.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
