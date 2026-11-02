"""Load named catalogs and external tables once, with source provenance."""

from functools import lru_cache
from os import PathLike
from pathlib import Path

from stardew.domain.catalogs import ItemCatalog
from stardew.domain.models import freeze
from stardew.domain.models.game_data import GameData
from stardew.domain.predictions.artifact_conditions import validate_artifact_tables
from stardew.resources import data_path

from ..data_files import DataError, read_json


@lru_cache(maxsize=1)
def bundled_catalogs():
    catalogs = freeze(read_json(data_path("catalogs").joinpath("rules.json")))
    names = read_json(data_path("catalogs").joinpath("item_names.json"))
    return catalogs, ItemCatalog(
        freeze(names["objects"]), freeze(names["bigCraftables"])
    )


@lru_cache(maxsize=1)
def bundled_maps():
    from .maps import read_maps

    return freeze(read_maps(data_path("maps.json")))


def load_game_data(
    directory: str | PathLike[str] | None = None,
    *,
    resources: str | PathLike[str] | None = None,
    include_maps: bool = True,
) -> GameData:
    if not isinstance(include_maps, bool):
        raise TypeError("include_maps must be a Boolean")
    if not include_maps and resources is not None:
        raise ValueError("resources requires include_maps=True")
    catalogs, items = bundled_catalogs()
    if not include_maps:
        maps = freeze({})
        map_provenance = {"loaded": False}
    elif resources is None:
        maps = bundled_maps()
        map_provenance = read_json(data_path("maps.provenance.json"))
    else:
        from .maps import read_maps

        maps = freeze(read_maps(resources))
        map_provenance = {"source": str(Path(resources).expanduser().resolve())}
    tables, provenance = (
        {},
        {
            "catalogs": "MouseyPounds checkup 8e48aa1 / predictor b9e7c71",
            "maps": map_provenance,
        },
    )
    if directory is not None:
        directory = Path(directory).expanduser().resolve()
        manifest_path = directory / "manifest.json"
        manifest = read_json(manifest_path) if manifest_path.exists() else None
        filenames = {
            name + ".json"
            for name in ("Objects", "Locations", "ObjectNames", "provenance")
        }
        optional = {
            name + ".json"
            for name in (
                "Shops",
                "Characters",
                "GarbageCans",
                "LocationContexts",
                "MakeoverOutfits",
            )
        }
        if manifest is not None and (
            not isinstance(manifest, dict)
            or manifest.get("format_version") != 1
            or manifest.get("game_version") != "1.6.15"
            or not isinstance(manifest.get("locale"), str)
            or not isinstance(manifest.get("files"), dict)
            or not filenames <= set(manifest["files"]) <= filenames | optional
            or any(
                not isinstance(digest, str)
                or len(digest) != 64
                or any(c not in "0123456789abcdefABCDEF" for c in digest)
                for digest in manifest["files"].values()
            )
        ):
            raise DataError(f"Invalid export manifest: {manifest_path}")
        for name in ("Objects", "Locations", "ObjectNames", "provenance"):
            path = directory / (name + ".json")
            if not path.is_file():
                raise DataError(f"Missing exported game table: {path}")
            tables[name] = read_json(
                path, expected_sha256=manifest["files"][path.name] if manifest else None
            )
            if not isinstance(tables[name], dict) or not tables[name]:
                raise DataError(f"Invalid exported game table: {path.name}")
        source = tables.pop("provenance")
        extra_catalogs = {}
        for filename in sorted(optional):
            path = directory / filename
            if manifest is not None and filename not in manifest["files"]:
                continue
            if not path.exists() and manifest is None:
                continue
            value = read_json(
                path, expected_sha256=manifest["files"][filename] if manifest else None
            )
            if (
                not isinstance(
                    value, list if filename == "MakeoverOutfits.json" else dict
                )
                or not value
            ):
                raise DataError(f"Invalid prediction table: {path}")
            extra_catalogs["game_" + path.stem] = value
        if extra_catalogs:
            catalogs = freeze({**catalogs, **extra_catalogs})
        if not isinstance(source.get("sources"), dict) or not source["sources"]:
            raise DataError("Game table provenance must identify source hashes.")
        try:
            validate_artifact_tables(tables)
        except (TypeError, ValueError) as error:
            raise DataError(
                f"Invalid exported game data in {directory}: {error}"
            ) from error
        if manifest is not None:
            source["manifest"] = manifest
        source["manifest_verified"] = manifest is not None
        provenance["game_tables"] = {"directory": str(directory), **source}
    return GameData(catalogs, items, maps, freeze(tables), freeze(provenance))
