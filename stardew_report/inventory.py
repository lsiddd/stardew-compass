"""List saved inventory slots and chest contents without changing the save."""

from .data import load_data

XSI = "{http://www.w3.org/2001/XMLSchema-instance}"
QUALITIES = {"0": "normal", "1": "silver", "2": "gold", "4": "iridium"}


def present(node):
    return node is not None and node.get(XSI + "nil") not in ("true", "1") and len(node) > 0


def item_text(item, names):
    identifier = item.findtext("itemId") or item.findtext("parentSheetIndex") or ""
    kind = item.get(XSI + "type", item.tag).split(":")[-1]
    table = None
    if identifier.startswith("(BC)") or item.findtext("bigCraftable") == "true":
        table = "bigCraftables"
    elif identifier.startswith("(O)") or kind in ("Item", "Object", "ColoredObject"):
        table = "objects"
    lookup = identifier.split(")", 1)[-1] if identifier.startswith("(") else identifier
    label = item.findtext("name")
    if not label and table:
        label = names[table].get(lookup)
    label = label or ("#" + identifier if identifier else kind)
    quantity = item.findtext("stack") or "1"
    quality = item.findtext("quality") or "0"
    details = [f"quality: {QUALITIES.get(quality, quality)}"]
    if identifier:
        details.append(f"ID: {identifier}")
    if item.findtext("isRecipe") == "true":
        details.append("recipe")
    return f"{label} x{quantity} ({'; '.join(details)})"


def slot_lines(container, names, indent=""):
    lines = []
    if container is not None:
        for slot, item in enumerate(container, 1):
            if not present(item):
                continue
            lines.append(f"{indent}* Slot {slot}: {item_text(item, names)}")
            attachments = slot_lines(item.find("attachments"), names, indent + "    ")
            if attachments:
                lines.append(indent + "  Attachments:")
                lines.extend(attachments)
    return lines


def chest_location(chest, farmers):
    parts = []
    for node in reversed(list(chest.iterancestors())):
        if node.tag in ("GameLocation", "indoors"):
            parts.append(node.findtext("uniqueName") or node.findtext("name") or node.get(XSI + "type", node.tag))
        elif node.tag == "Building":
            kind = node.findtext("buildingType") or "Building"
            parts.append(f"{kind} ({node.findtext('tileX', '?')}, {node.findtext('tileY', '?')})")
        elif node in farmers:
            parts.append(f"Inventory: {node.findtext('name')}")
        elif node.get(XSI + "type", "").split(":")[-1] == "Chest":
            parts.append("inside " + (node.findtext("name") or "Chest"))
    # A placed object's dictionary key is authoritative; tileLocation may be stale.
    parent = chest.getparent()
    tile = None
    if parent is not None and parent.tag == "value":
        tile = parent.getparent().find("key/Vector2")
    if tile is None:
        tile = chest.find("tileLocation")
    if tile is not None:
        parts.append(f"tile ({tile.findtext('X', '?')}, {tile.findtext('Y', '?')})")
    return " / ".join(parts) or chest.getroottree().getpath(chest)


def inventory_text(root, farmers):
    names = load_data("item_names")
    out = []
    for farmer in farmers:
        out.append(f"\nInventory: {farmer.findtext('name')}\n")
        out.extend(slot_lines(farmer.find("items"), names) or ["* Empty"])
        equipped = []
        for field in ("hat", "shirtItem", "pantsItem", "boots", "leftRing", "rightRing", "trinketItems"):
            item = farmer.find(field)
            if not present(item):
                continue
            if field == "trinketItems":
                equipped.extend(slot_lines(item, names))
            else:
                equipped.append(f"* {field}: {item_text(item, names)}")
        if equipped:
            out.extend(["\nEquipped:", *equipped])

    chests = [
        node for node in root.iter()
        if present(node) and (
            node.get(XSI + "type", "").split(":")[-1] == "Chest"
            or node.tag == "Chest"
            or (node.tag == "fridge" and node.find("items") is not None)
        )
    ]
    out.append(f"\nChests and fridges: {len(chests)}\n")
    if not chests:
        out.append("* None")
    for number, chest in enumerate(chests, 1):
        label = chest.findtext("name") or ("Fridge" if chest.tag == "fridge" else "Chest")
        custom = chest.xpath(
            "string(./modData/item[key/string='Pathoschild.ChestsAnywhere/Name']/value/string)"
        )
        if custom:
            label = f"{custom} ({label})"
        out.append(f"\nChest {number}: {label} — {chest_location(chest, farmers)}\n")
        shared = chest.findtext("globalInventoryId/string") or chest.findtext("globalInventoryId")
        if shared and shared.strip():
            out.append(f"* Shared inventory: {shared} (listed below)")
        else:
            out.extend(slot_lines(chest.find("items"), names) or ["* Empty"])
        for entry in chest.findall("separateWalletItems//item"):
            owner = entry.findtext("key/long")
            if owner is None:
                continue
            out.append(f"  Separate wallet inventory: {owner}")
            container = entry.find("value/Inventory")
            out.extend(slot_lines(container, names, "  ") or ["  * Empty"])

    # Shared storage is listed once rather than counted again at each linked chest.
    for entry in root.findall("globalInventories/item"):
        label = entry.findtext("key/string") or "Unknown"
        out.append(f"\nShared inventory: {label}\n")
        out.extend(slot_lines(entry.find("value/Inventory"), names) or ["* Empty"])
    return "\n".join(out).strip()
