"""Read the saved tool facts needed by the unmodified enchantment rules."""

_TOOLS = {
    "MeleeWeapon": "Weapon",
    "Pickaxe": "Pickaxe",
    "Axe": "Axe",
    "Hoe": "Hoe",
    "WateringCan": "Watering Can",
    "FishingRod": "Fishing Rod",
    "Pan": "Pan",
}
_NAMES = {
    "ArtfulEnchantment": "Artful",
    "BugKillerEnchantment": "Bug Killer",
    "VampiricEnchantment": "Vampiric",
    "CrusaderEnchantment": "Crusader",
    "HaymakerEnchantment": "Haymaker",
    "PowerfulEnchantment": "Powerful",
    "ReachingToolEnchantment": "Reaching",
    "ShavingEnchantment": "Shaving",
    "BottomlessEnchantment": "Bottomless",
    "GenerousEnchantment": "Generous",
    "ArchaeologistEnchantment": "Archaeologist",
    "MasterEnchantment": "Master",
    "AutoHookEnchantment": "Auto Hook",
    "PreservingEnchantment": "Preserving",
    "EfficientToolEnchantment": "Efficient",
    "SwiftToolEnchantment": "Swift",
    "FisherEnchantment": "Fisher",
}
_HISTORY_NAMES = {"Expansive": "Reaching", "Auto-Hook": "Auto Hook"}
_XSI_NIL = "{http://www.w3.org/2001/XMLSchema-instance}nil"


def saved_enchantment_tools(player):
    """Preserve XmlElement history order; omitted empty lists mean no history."""
    result = []
    for item in player.inventory:
        label = _TOOLS.get(item.kind)
        item_id = item.item_id or ""
        if (
            label is None
            or label == "Weapon"
            and item_id.removeprefix("(W)")
            in {
                "47",
                "53",
                "66",
            }
        ):
            continue
        node = item.snapshot
        upgrade = node.value("upgradeLevel")
        previous = []
        for entry in node.findall("previousEnchantments"):
            # The real serializer repeats <previousEnchantments>text</...>.
            # Wrapped <string> fixtures remain supported without reordering.
            entries = entry.findall("string") if entry.children else (entry,)
            previous.extend(child.text() for child in entries if child.text())
        history_known = not any(
            entry.get(_XSI_NIL) in ("true", "1")
            for tag in ("enchantments", "previousEnchantments")
            for entry in node.findall(tag)
        )
        result.append(
            {
                "tool": label,
                "slot": item.slot,
                "itemId": item_id
                if item_id.startswith("(")
                else f"({'W' if label == 'Weapon' else 'T'}){item_id}"
                if item_id
                else None,
                "name": item.name,
                "upgradeLevel": int(upgrade) if upgrade is not None else None,
                "current": tuple(
                    _NAMES[name] for name in sorted(item.enchantments) if name in _NAMES
                ),
                "previous": tuple(_HISTORY_NAMES.get(name, name) for name in previous),
                "historyKnown": history_known,
            }
        )
    return tuple(result)


def eligible_enchantments(pool, current=(), previous=(), upgrade_level=4):
    """Mirror BaseEnchantment.GetAvailableEnchantmentsForItem's ordered filter."""
    result = [
        name
        for name in pool
        if name not in current and (name != "Reaching" or upgrade_level == 4)
    ]
    for name in previous:
        if len(result) <= 1:
            break
        result = [candidate for candidate in result if candidate != name]
    return tuple(result)
