"""Direct XML implementation of the extra stardew.app report fields (MIT).

Unlike the original whole-app parser, these fields work independently and
single-animal buildings do not disappear because of XML array cardinality.
"""

from .data import load_data

SKILLS = ("farming", "fishing", "foraging", "mining", "combat")
XSI = "{http://www.w3.org/2001/XMLSchema-instance}type"


def int_field(element, path, default=0):
    return int(element.findtext(path) or default)


def players(root):
    host = root.find("player")
    yield host
    seen = {host.findtext("UniqueMultiplayerID")}
    candidates = [*root.findall("./farmhands/Farmer"), *root.findall(".//farmhand")]
    for player in candidates:
        identifier = player.findtext("UniqueMultiplayerID")
        if player.findtext("name") and identifier not in seen:
            seen.add(identifier)
            yield player


def extras_text(root):
    names = load_data("item_names")
    farmers = list(players(root))
    out = []
    for player in farmers:
        who = player.findtext("name") + ": " if len(farmers) > 1 else ""
        out.append(
            f"\n{who}Skill experience (Checkup reports only the xp still needed)\n"
        )
        experience = [int(n.text or 0) for n in player.findall("experiencePoints/int")]
        for i, skill in enumerate(SKILLS):
            xp = experience[i] if i < len(experience) else 0
            out.append(
                f"* {skill.capitalize():<9} {xp:>9,} xp   (level {int_field(player, skill + 'Level')})"
            )
        shipped = []
        for item in player.findall("basicShipped/item"):
            identifier = item.findtext("key/string") or item.findtext("key/int") or ""
            if identifier.startswith("(O)"):
                identifier = identifier[3:]
            shipped.append(
                (
                    identifier,
                    names["objects"].get(identifier, "#" + identifier),
                    int_field(item, "value/int"),
                )
            )
        # Match JS object enumeration before the stable quantity sort.
        shipped.sort(
            key=lambda row: (0, int(row[0])) if row[0].isdigit() else (1, row[0])
        )
        shipped.sort(key=lambda row: -row[2])
        if shipped:
            out.append(
                f"\n{who}Quantity shipped per item (Checkup reports only which items are missing)\n"
            )
            width = max(len(label) for _, label, _ in shipped)
            out.extend(f"* {label:<{width}}  {qty:>6,}" for _, label, qty in shipped)
    rarecrows = set()
    for name in root.iter("name"):
        if name.text == "Rarecrow":
            identifier = name.getparent().findtext("parentSheetIndex")
            if identifier:
                rarecrows.add(identifier)
    labels = sorted(names["bigCraftables"].get(id, "#" + id) for id in rarecrows)
    out.extend(
        [
            f"\nRarecrows found in the save: {len(labels)} of 8\n",
            "* " + (", ".join(labels) or "none"),
            "! Counts rarecrows currently placed or stored, so one that was sold or",
            "  destroyed after collecting still breaks the set.",
        ]
    )
    animals = []
    for location in root.findall("locations/GameLocation"):
        if location.get(XSI) != "Farm":
            continue
        for building in location.findall("buildings/Building"):
            indoors = building.find("indoors")
            if indoors is not None and indoors.get(XSI) == "AnimalHouse":
                container = indoors.find("animals")
                if container is None:
                    container = indoors.find("Animals")
                if container is not None:
                    animals.extend(container.findall(".//FarmAnimal"))
    if animals:
        out.append("\nFarm animals (Checkup reports names and cracker status only)\n")
        width = max(len(a.findtext("name") or "Unknown") for a in animals)
        for animal in animals:
            name = animal.findtext("name") or "Unknown"
            kind = animal.findtext("type") or "Unknown"
            out.append(
                f"* {name:<{width}}  {kind:<15} {int_field(animal, 'age'):>4} days  "
                f"friendship {int_field(animal, 'friendshipTowardFarmer'):>4}  happiness {int_field(animal, 'happiness'):>3}"
            )
    out.append(f"\nPerfection waivers used: {int_field(root, 'perfectionWaivers')}")
    return "\n".join(out).strip()
