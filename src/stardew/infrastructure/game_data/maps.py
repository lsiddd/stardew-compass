"""Geometry adapted from the original StardewValley.Tiled/Map.cs."""

import json
import xml.etree.ElementTree as ET
from pathlib import Path

from stardew.domain.models.maps import Map

from ..data_files import MAX_DATA_BYTES, DataError, read_json
from ..streams import read_bounded


def read_maps(path, names=None):
    """Read packaged JSON maps or an external legacy RESX resource."""
    source = path if hasattr(path, "open") else Path(path).expanduser()
    try:
        if getattr(source, "name", str(source)).endswith(".resx"):
            with source.open("rb") as stream:
                payload = read_bounded(stream, MAX_DATA_BYTES)
            if len(payload) > MAX_DATA_BYTES:
                raise ValueError("exceeds the 64 MiB data limit")
            values = {
                element.get("name"): json.loads(element.findtext("value"))
                for element in ET.fromstring(payload).findall("data")
                if names is None or element.get("name") in names
            }
        else:
            values = read_json(source)
        if not isinstance(values, dict):
            raise ValueError("expected an object mapping location names to maps")
        result = {}
        for name, data in values.items():
            if names is None or name in names:
                try:
                    result[name] = Map({**data, "Name": data.get("Name") or name})
                except (KeyError, TypeError, ValueError) as error:
                    raise ValueError(f"location {name}: {error}") from error
        return result
    except (ET.ParseError, ValueError, TypeError) as error:
        raise DataError(f"Invalid map resource {source}: {error}") from error
