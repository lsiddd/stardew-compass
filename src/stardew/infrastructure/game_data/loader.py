"""Load named catalogs and external tables once, with source provenance."""

from functools import lru_cache
from os import PathLike
from pathlib import Path
import json

from stardew.domain.models import freeze
from stardew.domain.models.game_data import GameData
from stardew.domain.catalogs import ItemCatalog
from stardew.resources import data_path


class DataError(ValueError):
    pass


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeError) as error:
        raise DataError(f"Invalid game table {path.name}: {error}") from error


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
) -> GameData:
    catalogs, items = bundled_catalogs()
    if resources is None:
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
        for name in ("Objects", "Locations", "ObjectNames", "provenance"):
            path = directory / (name + ".json")
            if not path.is_file():
                raise DataError(f"Missing exported game table: {path}")
            tables[name] = read_json(path)
            if not isinstance(tables[name], dict) or not tables[name]:
                raise DataError(f"Invalid exported game table: {path.name}")
        source = tables.pop("provenance")
        if not isinstance(source.get("sources"), dict) or not source["sources"]:
            raise DataError("Game table provenance must identify source hashes.")
        provenance["game_tables"] = {"directory": str(directory), **source}
    return GameData(catalogs, items, maps, freeze(tables), freeze(provenance))
