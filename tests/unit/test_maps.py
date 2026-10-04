import pytest
from stardew.infrastructure.game_data.maps import Map


def test_geometry_preserves_first_layer_and_strict_firstgid():
    layer = {"name": "Back", "width": 2, "data": [1, 2]}
    map = Map(
        {
            "width": 2,
            "height": 1,
            "layers": [layer, {"name": "Back"}],
            "tilesets": [
                {
                    "firstgid": 1,
                    "tiles": [
                        {"id": 0, "properties": [{"name": "Water"}]},
                        {"id": 1, "properties": [{"name": "Water", "value": False}]},
                    ],
                }
            ],
        }
    )
    assert map.tile(1) is None
    assert map.property(1, 0, "Water")
    assert map.index(0, 2, "Back") == 0
    with pytest.raises(IndexError):
        map.index(-1, 0, "Back")


@pytest.mark.parametrize("suffix", [".json", ".resx"])
def test_read_map_resource_formats(tmp_path, suffix):
    import json
    import xml.etree.ElementTree as ET
    from stardew.infrastructure.game_data.maps import read_maps

    data = {"width": 2, "height": 1, "layers": [], "tilesets": []}
    path = tmp_path / ("maps" + suffix)
    if suffix == ".json":
        path.write_text(json.dumps({"Town": data, "Forest": data}))
    else:
        root = ET.Element("root")
        for name in ("Town", "Forest"):
            entry = ET.SubElement(root, "data", name=name)
            ET.SubElement(entry, "value").text = json.dumps(data)
        ET.ElementTree(root).write(path, encoding="utf-8")
    for source in (path, str(path)):
        maps = read_maps(source, ["Town"])
        assert list(maps) == ["Town"]
        assert maps["Town"].width == 2
        assert maps["Town"].height == 1
