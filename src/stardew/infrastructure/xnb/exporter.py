"""Read-only game data export. Decode and validate all inputs before writing."""

import hashlib
import json
from pathlib import Path

from ..files import atomic_write_many
from .reader import Reader, read_xnb_bytes, unpack_xnb

TABLES = [
    ("Content/Data/Objects.xnb", "Objects.json"),
    ("Content/Data/Locations.xnb", "Locations.json"),
    ("Content/Strings/Objects.pt-BR.xnb", "ObjectNames.json"),
]
PREDICTION_TABLES = {
    "Shops": "System.Collections.Generic.Dictionary`2<System.String|StardewValley.GameData.Shops.ShopData>",
    "Characters": "System.Collections.Generic.Dictionary`2<System.String|StardewValley.GameData.Characters.CharacterData>",
    "GarbageCans": "StardewValley.GameData.GarbageCans.GarbageCanData",
    "LocationContexts": "System.Collections.Generic.Dictionary`2<System.String|StardewValley.GameData.LocationContexts.LocationContextData>",
    "MakeoverOutfits": "System.Collections.Generic.List`1<StardewValley.GameData.MakeoverOutfits.MakeoverOutfit>",
}


def export_game_data(game, output):
    game, output = Path(game).resolve(), Path(output).resolve()
    # Prevent accidental writes anywhere within the original game installation.
    if output == game or game in output.parents:
        raise ValueError("Output directory must be outside the game installation.")
    with (game / "Stardew Valley.dll").open("rb") as stream:
        hashes = {
            "Stardew Valley.dll": hashlib.file_digest(stream, "sha256")
            .hexdigest()
            .upper()
        }
    tables = {}
    for source, target in TABLES:
        data = read_xnb_bytes(game / source)
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
    for name, expected in PREDICTION_TABLES.items():
        source = f"Content/Data/{name}.xnb"
        if not (game / source).exists():
            continue  # Compatibility with minimal/older exports.
        data = read_xnb_bytes(game / source)
        hashes[source] = hashlib.sha256(data).hexdigest().upper()
        tables[name + ".json"] = Reader(unpack_xnb(data)).read(expected)
    tables["provenance.json"] = {"sources": hashes}
    encoded = {
        name: json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False).encode(
            "utf-8"
        )
        for name, data in tables.items()
    }
    manifest = json.dumps(
        {
            "format_version": 1,
            "game_version": "1.6.15",
            "locale": "pt-BR",
            "files": {
                name: hashlib.sha256(payload).hexdigest()
                for name, payload in encoded.items()
            },
        },
        indent=2,
    ).encode("utf-8")
    # Publish the manifest first: a failed multi-file replacement is detected by
    # readers, including when exporting into a previously empty directory.
    atomic_write_many(
        {
            output / "manifest.json": manifest,
            **{output / name: payload for name, payload in encoded.items()},
        }
    )
    return (output / "manifest.json", *(output / name for name in encoded))


export = export_game_data
