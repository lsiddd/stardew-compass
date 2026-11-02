"""Prepare shared saved-object lookups without exposing an XML tree."""

from collections import defaultdict

from stardew.domain.models.state import SaveIndex, SaveNode, freeze


def build_index(root: SaveNode) -> SaveIndex:
    tags = defaultdict(list)
    objects = defaultdict(list)
    default_statues = set()
    characters = []
    for node in root.iter():
        if node.tag in ("FarmAnimal", "NPC", "farmhand"):
            tags[node.tag].append(node)
        if node.tag == "characters":
            characters.extend(child for child in node.children if child.tag == "NPC")
        if node.tag in ("Item", "Object", "Chest", "fridge"):
            name = node.value("name")
            if name:
                objects[name].append(node)
    for location in root.findall("locations/*"):
        if location.value("name") != "Town":
            continue
        for entry in location.findall(".//item"):
            node = entry.find("value/Object")
            if (
                node is not None
                and node.value("name") == "Stone Junimo"
                and entry.value("key/Vector2/X") == "57"
                and entry.value("key/Vector2/Y") == "16"
            ):
                default_statues.add(id(node))
    return SaveIndex(
        freeze(tags), freeze(objects), frozenset(default_statues), tuple(characters)
    )
