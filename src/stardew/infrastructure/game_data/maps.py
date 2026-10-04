"""Geometry adapted from the original StardewValley.Tiled/Map.cs."""

from stardew.domain.models.maps import Map

import json
from pathlib import Path
import xml.etree.ElementTree as ET


def read_maps(path, names=None):
    """Read packaged JSON maps or an external legacy RESX resource."""
    if getattr(path, "name", str(path)).endswith(".resx"):
        values = {
            e.get("name"): json.loads(e.findtext("value"))
            for e in ET.parse(path).getroot().findall("data")
            if names is None or e.get("name") in names
        }
    else:
        # Traversable resources and normal filesystem paths share the same reader.
        source = path if hasattr(path, "read_text") else Path(path)
        values = json.loads(source.read_text(encoding="utf-8"))
    return {
        name: Map(data)
        for name, data in values.items()
        if names is None or name in names
    }
