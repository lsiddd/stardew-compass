QUALITIES = {0: "normal", 1: "silver", 2: "gold", 4: "iridium"}
SKILLS = ("farming", "fishing", "foraging", "mining", "combat", "luck")


def item_text(item, data):
    label = item.name or data.items.name(
        item.item_id, kind=item.kind, big_craftable=item.big_craftable
    )
    quality = item.quality if item.quality is not None else 0
    details = [f"quality: {QUALITIES.get(quality, quality)}"]
    if item.item_id:
        details.append(f"ID: {item.item_id}")
    if item.is_recipe:
        details.append("recipe")
    return f"{label} x{item.quantity if item.quantity is not None else 1} ({'; '.join(details)})"


def slot_lines(items, data, indent=""):
    lines = []
    for item in items:
        lines.append(f"{indent}* Slot {item.slot}: {item_text(item, data)}")
        if item.attachments:
            lines.extend(
                [
                    indent + "  Attachments:",
                    *slot_lines(item.attachments, data, indent + "    "),
                ]
            )
    return lines


def render_extras(result, data):
    out = []
    for player in result.players:
        out.extend(
            [
                f"\nInventory: {player.name}\n",
                *(slot_lines(player.inventory, data) or ["* Empty"]),
            ]
        )
        if player.equipment:
            out.append("\nEquipped:\n")
            for field, items in player.equipment.items():
                out.extend(
                    slot_lines(items, data)
                    if field == "trinketItems"
                    else [f"* {field}: {item_text(item, data)}" for item in items]
                )
    out.append(f"\nChests and fridges: {len(result.containers)}\n")
    if not result.containers:
        out.append("* None")
    for number, chest in enumerate(result.containers, 1):
        out.append(f"\nChest {number}: {chest.name} — {chest.location}\n")
        if chest.shared_inventory:
            out.append(f"* Shared inventory: {chest.shared_inventory} (listed below)")
        else:
            out.extend(slot_lines(chest.inventory, data) or ["* Empty"])
        for owner, items in chest.wallets.items():
            out.extend(
                [
                    f"  Separate wallet inventory: {owner}",
                    *(slot_lines(items, data, "  ") or ["  * Empty"]),
                ]
            )
    for name, items in result.shared_inventories.items():
        out.extend(
            [f"\nShared inventory: {name}\n", *(slot_lines(items, data) or ["* Empty"])]
        )
    for player in result.players:
        who = player.name + ": " if len(result.players) > 1 else ""
        out.append(f"\n{who}Skill experience\n")
        for index, skill in enumerate(SKILLS):
            xp = player.experience[index] if index < len(player.experience) else 0
            level = player.skills.get(skill)
            out.append(
                f"* {skill.capitalize():<9} {xp:>9,} xp   (level {level if level is not None else 'unknown'})"
            )
        if player.shipped:
            out.append(f"\n{who}Quantity shipped per item\n")
            width = max(len(item.name) for item in player.shipped)
            out.extend(
                f"* {item.name:<{width}}  {item.quantity:>6,}"
                for item in player.shipped
            )
    out.extend(
        [
            f"\nRarecrows found in the save: {len(result.rarecrows)} of 8\n",
            "* " + (", ".join(result.rarecrows) or "none"),
        ]
    )
    if result.animals:
        out.append("\nFarm animals\n")
        for animal in result.animals:
            out.append(
                f"* {animal.name or 'Unknown'}  {animal.kind or 'Unknown'}  {animal.age if animal.age is not None else '?'} days  "
                f"friendship {animal.friendship if animal.friendship is not None else '?'}  happiness {animal.happiness if animal.happiness is not None else '?'}"
            )
    out.append(
        f"\nPerfection waivers used: {result.perfection_waivers if result.perfection_waivers is not None else 'unknown'}"
    )
    return "\n".join(out).strip()
