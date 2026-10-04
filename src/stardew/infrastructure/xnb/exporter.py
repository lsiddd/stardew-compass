"""Read-only game data export. Decode and validate all inputs before writing."""

import hashlib
import json
from pathlib import Path
from .reader import Reader, unpack_xnb
from ..files import atomic_write_many

TABLES = [
    ("Content/Data/Objects.xnb", "Objects.json"),
    ("Content/Data/Locations.xnb", "Locations.json"),
    ("Content/Strings/Objects.pt-BR.xnb", "ObjectNames.json"),
]


def export_game_data(game, output):
    game, output = Path(game).resolve(), Path(output).resolve()
    # Prevent accidental writes anywhere within the original game installation.
    if output == game or game in output.parents:
        raise ValueError("Output directory must be outside the game installation.")
    hashes = {
        "Stardew Valley.dll": hashlib.sha256((game / "Stardew Valley.dll").read_bytes())
        .hexdigest()
        .upper()
    }
    tables = {}
    for source, target in TABLES:
        data = (game / source).read_bytes()
        hashes[source] = hashlib.sha256(data).hexdigest().upper()
        value_type = {
            "Objects.json": "StardewValley.GameData.Objects.ObjectData",
            "Locations.json": "StardewValley.GameData.Locations.LocationData",
            "ObjectNames.json": "System.String",
        }[target]
        expected = (
            "System.Collections.Generic.Dictionary`2<System.String|" + value_type + ">"
        )
        table = Reader(unpack_xnb(data)).read(expected)
        if not isinstance(table, dict) or not table:
            raise ValueError(f"Invalid exported table: {source}")
        tables[target] = table
    tables["provenance.json"] = {"sources": hashes}
    encoded = {
        name: json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False)
        for name, data in tables.items()
    }
    atomic_write_many(
        {output / name: data.encode("utf-8") for name, data in encoded.items()}
    )
    return tuple(output / name for name in encoded)


export = export_game_data
