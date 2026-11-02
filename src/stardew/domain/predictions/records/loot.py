"""Feature-local conversion of calculated facts to public prediction records."""

from ..loot.tool_state import eligible_enchantments
from ..report_models import PredictionAlternative, PredictionFact, PredictionRecord
from .common import product_id as _product_id


def build_geode(draft, context, identities):
    section = draft.section
    counters = (
        context.geodes_cracked if section == "geode" else context.mystery_boxes_opened
    )
    player = int(draft.facts.get("whichPlayer", context.player_index))
    if player < len(counters):
        draft.facts["saved_counter"] = counters[player]
        draft.facts["openings_ahead"] = int(draft.sequence) - counters[player]
    column = int(draft.facts["c"])
    draft.item, draft.quantity = (
        draft.facts["item"][column],
        draft.facts["itemQty"][column],
    )
    draft.facts["item_id"] = draft.facts.get(
        "itemIDs", [None] * len(draft.facts["item"])
    )[column]
    draft.facts["container"] = (
        (
            "Geode",
            "Frozen Geode",
            "Magma Geode",
            "Omni Geode",
            "Artifact Trove",
            "Golden Coconut",
        )[column]
        if section == "geode"
        else (
            "Mystery Box",
            "Golden Mystery Box without Farming Mastery",
            "Golden Mystery Box with Farming Mastery",
        )[column]
    )
    draft.alternatives.extend(
        PredictionAlternative(*values)
        for values in draft.facts.pop("dropAlternatives", ())
    )
    seed_result = draft.facts.pop("seedResult", None)
    if seed_result:
        draft.item = seed_result["name"]
        draft.facts["item_id"] = seed_result["item_id"]
    if section == "mystery" and draft.facts.get("requiresFishingLevel"):
        draft.alternatives.append(
            PredictionAlternative(
                "Unmodified Fishing level below 6", "(O)242", "Dish O'The Sea", 2
            )
        )


def build_raccoon(draft, context, identities):
    result = []
    for slot in range(3):
        delivered = draft.facts.get("deliveredSlots", ())
        if slot < 2 and slot < len(delivered) and delivered[slot]:
            continue
        name, amount = (draft.facts["bundleItem"][slot], draft.facts["bundleQty"][slot])
        seasonal = ()
        if isinstance(name, (list, tuple)):
            season = draft.facts.get("requestSeason")
            if season in (0, 1, 2, 3):
                name = name[season]
            else:
                seasonal = tuple(
                    (
                        PredictionAlternative(
                            f"Request season fixed at activation: {season}",
                            _product_id(choice, identities),
                            choice,
                            int(amount) if str(amount).isdigit() else None,
                        )
                        for season, choice in zip(
                            ("spring", "summer", "fall", "winter"), name, strict=False
                        )
                    )
                )
                name = None
        if isinstance(name, str) and " OR " in name:
            seasonal = tuple(
                (
                    PredictionAlternative(
                        "Depends on unshipped collections",
                        _product_id(choice, identities),
                        choice,
                        int(alternative_quantity),
                    )
                    for choice, alternative_quantity in zip(
                        name.split(" OR "), str(amount).split(" OR "), strict=False
                    )
                )
            )
            name = None
        if slot == 2 and draft.facts.get("rewardAlternatives"):
            seasonal = tuple(
                PredictionAlternative(*values)
                for values in draft.facts["rewardAlternatives"]
            )
            name = None
        result.append(
            PredictionRecord(
                sequence=int(draft.sequence),
                item_id="(H)RaccoonHat"
                if name == "Raccoon Hat"
                else _product_id(name, identities)
                if name
                else None,
                item_name=name,
                quantity=int(amount) if str(amount).isdigit() else None,
                alternatives=seasonal,
                facts=(
                    PredictionFact("role", "request" if slot < 2 else "reward"),
                    PredictionFact("slot", slot + 1),
                    *(
                        (
                            PredictionFact(
                                "request_state", draft.facts["requestState"]
                            ),
                            PredictionFact(
                                "request_season", draft.facts.get("requestSeason")
                            ),
                            PredictionFact(
                                "available_after_day",
                                draft.facts.get("availableAfterDay"),
                            ),
                            PredictionFact(
                                "conditions", draft.facts["requestConditions"]
                            ),
                        )
                        if "requestState" in draft.facts
                        else ()
                    ),
                ),
            )
        )
    return result


def build_prize(draft, context, identities):
    draft.alternatives.extend(
        PredictionAlternative(*values)
        for values in draft.facts.pop("seedAlternatives", ())
    )


def build_enchant(draft, context, identities):
    result = []
    for tool_index, tool in enumerate(draft.facts["labels"]):
        pool = draft.facts["validEnchants"][tool_index]
        roll = draft.facts["randRoll"]
        selected = draft.facts["item"][tool_index][0]
        conditional = []
        if "Reaching" in pool:
            basic_pool = eligible_enchantments(pool, upgrade_level=0)
            conditional.append(
                PredictionAlternative(
                    "New tool below iridium upgrade, no enchantment history",
                    None,
                    basic_pool[int(roll * len(basic_pool))],
                )
            )
        for current in pool:
            possible = []
            for older in (None, *pool):
                if older == current:
                    continue
                eligible = eligible_enchantments(
                    pool, (current,), (current,) if older is None else (current, older)
                )
                outcome = eligible[int(roll * len(eligible))]
                if outcome not in possible:
                    possible.append(outcome)
            conditional.extend(
                PredictionAlternative(
                    f"Iridium tool with current enchantment {current}; one older enchantment unknown (candidate)",
                    None,
                    name,
                )
                for name in possible
            )
        result.append(
            PredictionRecord(
                sequence=int(draft.sequence),
                player_id=draft.player_id,
                item_name=selected,
                alternatives=tuple(conditional),
                facts=(
                    PredictionFact("tool", tool),
                    PredictionFact("fresh_enchantment", selected),
                    PredictionFact("scenario", "new_iridium_tool_without_history"),
                    PredictionFact(
                        "conditions",
                        "Generic tool type, iridium upgrade, no current or previous enchantments; not the saved inventory tool",
                    ),
                ),
            )
        )
    for tool in draft.facts.get("toolPredictions", ()):
        result.append(
            PredictionRecord(
                sequence=int(draft.sequence),
                player_id=draft.player_id,
                item_name=tool["selected"],
                facts=(
                    PredictionFact("tool", tool["tool"]),
                    PredictionFact("tool_slot", tool["slot"]),
                    PredictionFact("tool_item_id", tool["itemId"]),
                    PredictionFact("tool_name", tool["name"]),
                    PredictionFact("upgrade_level", tool["upgradeLevel"]),
                    PredictionFact("current_enchantments", tool["current"]),
                    PredictionFact("previous_enchantments", tool["previous"]),
                    PredictionFact("eligible_enchantments", tool["eligible"]),
                    PredictionFact("certainty", tool["certainty"]),
                    PredictionFact("scenario", "saved_inventory_tool"),
                    PredictionFact(
                        "conditions",
                        "Saved tool state unchanged before this global enchantment number; rows do not simulate re-enchanting the same tool. Missing history or upgrade data has no definite result",
                    ),
                ),
            )
        )
    return result
