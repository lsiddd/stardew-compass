"""Feature-local conversion of calculated facts to public prediction records."""


def build_gembirds(draft, context, identities):
    index = int(draft.facts["i"])
    draft.location = draft.facts["locs"][index]
    draft.facts = {
        "direction": draft.location,
        "bird": draft.facts["birds"][index],
        "gem": draft.facts["gems"][draft.facts["birds"][index]],
    }
    draft.item = draft.facts["gem"]


def build_makeover(draft, context, identities):
    if draft.facts.get("d") is not None:
        draft.day = draft.facts.get("day")
        if "racers" in draft.facts:
            draft.facts = {
                "racers": draft.facts["racers"][str(draft.facts["d"])],
                "vendors": tuple(
                    (
                        draft.facts["vendor"][str(slot)][int(draft.facts["d"])]
                        for slot in (1, 2)
                    )
                ),
                **{
                    key: draft.facts[key]
                    for key in ("availability", "conditions")
                    if key in draft.facts
                },
            }
    elif "parts" in draft.facts:
        draft.facts["kind"] = "cactus"


def build_winterstar(draft, context, identities):
    draft.day = (int(draft.facts["year"]) - 1) * 112 + 109
