"""Bounded read-once XML decoding into an immutable domain snapshot."""

from __future__ import annotations

from pathlib import Path
from os import PathLike
import zlib
import re
from lxml import etree

from stardew.domain.models import (
    SaveNode,
    SaveMetadata,
    GameState,
    PlayerState,
    ItemState,
    ContainerState,
    BuildingState,
    LocationState,
    AnimalState,
    WorldState,
    NpcState,
    freeze,
    dictionary,
)

MAX_SAVE_BYTES = 128 * 1024 * 1024
XSI = "{http://www.w3.org/2001/XMLSchema-instance}"
SKILLS = ("farming", "fishing", "foraging", "mining", "combat", "luck")


class SaveError(ValueError):
    """Invalid saved data or an unsafe output destination."""


def integer(node, path, default=None):
    value = node.value(path)
    if value is None or value == "":
        return default
    try:
        if re.fullmatch(r"[+-]?[0-9]+", value.strip()) is None:
            raise ValueError("not a decimal integer")
        return int(value)
    except ValueError as error:
        raise SaveError(f"Invalid integer in {path}: {value}") from error


def statistic_integer(raw, name):
    if re.fullmatch(r"[+-]?[0-9]+", raw.strip()) is None:
        raise SaveError(f"Invalid integer in player statistic {name}: {raw}")
    return int(raw)


def boolean(node, path):
    value = node.value(path)
    if value is None:
        return None
    if value.strip().lower() not in ("true", "false", "1", "0"):
        raise SaveError(f"Invalid Boolean in {path}: {value}")
    return value.strip().lower() in ("true", "1")


def game_version(root):
    raw = root.value("gameVersion")
    if raw is None:
        return None
    if re.fullmatch(r"[0-9]+(?:\.[0-9]+){1,3}", raw.strip()) is None:
        raise SaveError(f"Invalid game version: {raw}")
    return ".".join(str(int(part)) for part in raw.strip().split("."))


def snapshot(element):
    return SaveNode(
        element.tag,
        element.text,
        freeze(element.attrib),
        tuple(snapshot(child) for child in element if isinstance(child.tag, str)),
    )


def present(node):
    return (
        node is not None
        and node.get(XSI + "nil") not in ("true", "1")
        and len(node) > 0
    )


def item_state(node, slot):
    return ItemState(
        slot,
        node.value("itemId") or node.value("parentSheetIndex"),
        node.value("name"),
        node.get(XSI + "type", node.tag).split(":")[-1],
        integer(node, "stack"),
        integer(node, "quality"),
        boolean(node, "isRecipe"),
        boolean(node, "bigCraftable"),
        inventory(node.find("attachments")),
        frozenset(
            child.get(XSI + "type", child.tag).split(":")[-1]
            for child in node.findall("enchantments/*")
        ),
        node,
    )


def inventory(node):
    return tuple(
        item_state(child, slot)
        for slot, child in enumerate(node if node is not None else (), 1)
        if present(child)
    )


def player_state(node: SaveNode, legacy_stats: SaveNode | None = None) -> PlayerState:
    stats = {}
    stat_node = node.find("stats")
    stat_node = stat_node if stat_node is not None else legacy_stats
    if stat_node is not None:
        for child in stat_node:
            if not child.children and child.content is not None:
                try:
                    stats[child.tag] = int(child.content)
                except ValueError:
                    continue
        for key, value in dictionary(stat_node.find("Values")).items():
            scalar = value.children[0].text() if value.children else value.text()
            if scalar is not None:
                stats[key] = statistic_integer(scalar, key)
    equipped = {}
    for field in (
        "hat",
        "shirtItem",
        "pantsItem",
        "boots",
        "leftRing",
        "rightRing",
        "trinketItems",
    ):
        child = node.find(field)
        if present(child):
            equipped[field] = (
                inventory(child) if field == "trinketItems" else (item_state(child, 1),)
            )
    return PlayerState(
        node.value("name", "Unknown"),
        integer(node, "UniqueMultiplayerID"),
        node.value("farmName"),
        freeze(stats),
        inventory(node.find("items")),
        freeze(equipped),
        tuple(
            statistic_integer(child.text("0"), "experiencePoints")
            for child in node.findall("experiencePoints/int")
        ),
        freeze({skill: integer(node, skill + "Level") for skill in SKILLS}),
        frozenset(child.text("") for child in node.findall("mailReceived/*")),
        freeze(
            {
                key: dictionary(node.find(key))
                for key in (
                    "basicShipped",
                    "fishCaught",
                    "cookingRecipes",
                    "craftingRecipes",
                    "recipesCooked",
                    "mineralsFound",
                    "archaeologyFound",
                    "friendships",
                    "friendshipData",
                    "specialItems",
                )
            }
        ),
        dictionary(node.find("friendshipData")),
        node.findall("questLog/*"),
        node,
        gender=node.value("gender"),
        is_male=boolean(node, "isMale"),
        total_money_earned=integer(node, "totalMoneyEarned"),
        deepest_mine_level=integer(node, "deepestMineLevel"),
        house_upgrade_level=integer(node, "houseUpgradeLevel"),
        spouse=node.value("spouse"),
        has_special_charm=boolean(node, "hasSpecialCharm"),
        events=frozenset(child.text("") for child in node.findall("eventsSeen/*")),
        achievements=frozenset(
            child.text("") for child in node.findall("achievements/*")
        ),
        milliseconds_played=integer(node, "millisecondsPlayed"),
        use_separate_wallets=boolean(node, "useSeparateWallets"),
    )


def player_nodes(root):
    host = root.find("player")
    yield host
    seen = {host.value("UniqueMultiplayerID")}
    for node in (*root.findall("farmhands/Farmer"), *root.findall(".//farmhand")):
        identifier = node.value("UniqueMultiplayerID")
        if node.value("name") and (identifier is None or identifier not in seen):
            seen.add(identifier)
            yield node


def containers(root, farmers):
    found = []

    def walk(node, trail=(), parent=None, grandparent=None):
        parts = trail
        if node.tag in ("GameLocation", "indoors"):
            parts = (
                *parts,
                node.value("uniqueName")
                or node.value("name")
                or node.get(XSI + "type", node.tag),
            )
        elif node.tag == "Building":
            parts = (
                *parts,
                f"{node.value('buildingType', 'Building')} ({node.value('tileX', '?')}, {node.value('tileY', '?')})",
            )
        elif any(node is farmer for farmer in farmers):
            parts = (*parts, f"Inventory: {node.value('name')}")
        is_chest = present(node) and (
            node.get(XSI + "type", "").split(":")[-1] == "Chest"
            or node.tag == "Chest"
            or (node.tag == "fridge" and node.find("items") is not None)
        )
        if is_chest:
            tile = (
                grandparent.find("key/Vector2")
                if parent is not None
                and parent.tag == "value"
                and grandparent is not None
                else None
            )
            tile = tile if tile is not None else node.find("tileLocation")
            x, y = (
                (tile.value("X"), tile.value("Y")) if tile is not None else (None, None)
            )
            location = " / ".join(parts)
            if tile is not None:
                location += (
                    " / " if location else ""
                ) + f"tile ({x or '?'}, {y or '?'})"
            name = node.value("name") or ("Fridge" if node.tag == "fridge" else "Chest")
            custom = dictionary(node.find("modData")).get(
                "Pathoschild.ChestsAnywhere/Name"
            )
            if custom is not None:
                name = f"{custom.value('string', '')} ({name})"
            shared = node.value("globalInventoryId/string") or node.value(
                "globalInventoryId"
            )
            wallets = {
                entry.value("key/long"): inventory(entry.find("value/Inventory"))
                for entry in node.findall("separateWalletItems//item")
                if entry.value("key/long") is not None
            }
            found.append(
                ContainerState(
                    name,
                    location or "Saved storage",
                    x,
                    y,
                    inventory(node.find("items")),
                    shared.strip() if shared and shared.strip() else None,
                    freeze(wallets),
                    node,
                )
            )
            parts = (*parts, "inside " + (node.value("name") or "Chest"))
        for child in node:
            walk(child, parts, node, parent)

    walk(root)
    return tuple(found)


def from_snapshot(root: SaveNode, path: str | PathLike[str]) -> GameState:
    farmers = tuple(player_nodes(root))
    players = tuple(
        player_state(node, root.find("stats") if index == 0 else None)
        for index, node in enumerate(farmers)
    )
    luck = root.value("dailyLuck")
    game_id = integer(root, "uniqueIDForThisGame")
    if game_id is None or not -(1 << 63) <= game_id < (1 << 63):
        raise SaveError("uniqueIDForThisGame must be a signed 64-bit integer.")
    metadata = SaveMetadata(
        game_id,
        game_version(root),
        integer(root, "year"),
        root.value("currentSeason"),
        integer(root, "dayOfMonth"),
        players[0].stats.get("daysPlayed"),
        boolean(root, "useLegacyRandom"),
        integer(root, "whichFarm"),
        float(luck) if luck is not None else None,
    )
    locations = tuple(
        LocationState(
            node.value("name"),
            node.get(XSI + "type"),
            tuple(
                BuildingState(
                    building.value("buildingType"),
                    integer(building, "tileX"),
                    integer(building, "tileY"),
                    building,
                )
                for building in node.findall("buildings/Building")
            ),
            node,
            museum_items=tuple(
                item.text("") for item in node.findall("museumPieces/item/value/*")
            ),
        )
        for node in root.findall("locations/*")
    )
    animals, seen_animals = [], set()
    for node in root.iter("FarmAnimal"):
        animal_id = integer(node, "myID")
        # Saves can serialize the same herd under both animals and Animals.
        if animal_id is not None and animal_id in seen_animals:
            continue
        if animal_id is not None:
            seen_animals.add(animal_id)
        animals.append(
            AnimalState(
                node.value("name"),
                node.value("type"),
                integer(node, "age"),
                integer(node, "friendshipTowardFarmer"),
                integer(node, "happiness"),
                boolean(node, "hasEatenAnimalCracker"),
                node,
                animal_id,
            )
        )
    shared = {
        entry.value("key/string", "Unknown"): inventory(entry.find("value/Inventory"))
        for entry in root.findall("globalInventories/item")
    }
    world = WorldState(
        containers(root, farmers),
        freeze(shared),
        locations,
        tuple(animals),
        root.findall("specialOrders/*"),
        root,
        npcs=tuple(
            NpcState(npc.value("name"), frozenset(npc.attributes.values()))
            for npc in root.findall(".//characters/NPC")
        ),
        child_count=sum(
            "Child" in npc.attributes.values() for npc in root.findall(".//NPC")
        ),
        qi_crops_active=any(
            "DROP_QI_BEANS" in (order.value("specialRule") or "")
            for order in root.findall("specialOrders/*")
        ),
        mines_difficulty=integer(root, "minesDifficulty"),
        times_fed_raccoons=integer(root, "timesFedRaccoons"),
        visits_until_y1_guarantee=integer(root, "visitsUntilY1Guarantee"),
        perfection_waivers=integer(root, "perfectionWaivers"),
        applied_1_3_changes=boolean(root, "hasApplied1_3_UpdateChanges"),
        applied_1_4_changes=boolean(root, "hasApplied1_4_UpdateChanges"),
        treasure_totems_used=integer(root, "treasureTotemsUsed"),
        lost_books_found=integer(root, "lostBooksFound"),
        golden_coconut_cracked=boolean(root, "goldenCoconutCracked"),
        game_version_label=root.value("gameVersionLabel"),
    )
    return GameState(Path(path), metadata, players, world, root)


def resolve_save(value: str | PathLike[str]) -> Path:
    path = Path(value).expanduser().resolve()
    if path.is_dir():
        path = path / path.name
    if not path.is_file():
        raise SaveError(f"Save file does not exist: {path}")
    return path


def load_save(value: str | PathLike[str]) -> GameState:
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
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    data = data.lstrip(b" \t\r\n")
    try:
        element = etree.fromstring(
            data,
            parser=etree.XMLParser(
                resolve_entities=False, load_dtd=False, no_network=True
            ),
        )
    except etree.XMLSyntaxError as error:
        raise SaveError(f"Invalid save XML: {error.msg}") from error
    if element.getroottree().docinfo.doctype:
        raise SaveError("Save XML must not contain a DTD.")
    if element.tag != "SaveGame" or element.find("player") is None:
        raise SaveError(
            "Use the full farmer_ID save, not SaveGameInfo (which is only a summary)."
        )
    for field in ("player/name", "uniqueIDForThisGame"):
        if not element.findtext(field):
            raise SaveError(f"Save is missing the required field {field}.")
    return from_snapshot(snapshot(element), path)
