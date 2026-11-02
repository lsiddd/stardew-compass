"""Feature-local conversion of calculated facts to public prediction records."""


def build_trash(draft, context, identities):
    draft.item = draft.facts.get("trashItem")
    draft.quantity = draft.facts.get("stack") or 1
    draft.location = (
        "Jodi",
        "Emily",
        "Mayor",
        "Museum",
        "Blacksmith",
        "Saloon",
        "Alex",
        "Joja",
        "Desert Festival",
    )[int(draft.facts["whichCan"])]


def build_train(draft, context, identities):
    draft.facts["arrives"] = draft.facts.get("trainTime") is not None


def build_night(draft, context, identities):
    draft.facts["event"] = draft.facts.get("thisEvent")


def build_statue(draft, context, identities):
    if "coords" in draft.facts:
        draft.location = draft.facts["pbMaps"][int(draft.facts["index"])]
        draft.facts = {
            "coordinate_candidates": draft.facts["coords"],
            "prismatic_shard": draft.facts["shard"],
            "requires_clear_spawn_tile": True,
            "spawn_conditions": draft.facts.get("spawnConditions"),
        }
    else:
        draft.facts = {
            "blessing_rain": draft.facts["blessingNames"][
                int(draft.facts["blessRain"])
            ],
            "blessing_clear": draft.facts["blessingNames"][
                int(draft.facts["blessNoRain"])
            ],
            "dwarf_choices": (
                draft.facts["dwarfNames"][int(draft.facts["dwarf1"])],
                draft.facts["dwarfNames"][int(draft.facts["dwarf2"])],
            ),
            "effective_blessing": draft.facts.get("effectiveBlessing"),
            "is_festival": draft.facts.get("isFestival"),
            "weather_alternatives": draft.facts.get("weatherAlternatives"),
            "weather_source": draft.facts.get("weatherSource"),
            "conditions": draft.facts.get("conditions"),
        }
