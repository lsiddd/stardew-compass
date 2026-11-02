"""Shared, explicit record fields and immutable public facts."""

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from .. import report_support as rules
from ..report_models import (
    PredictionAlternative,
    PredictionDate,
    PredictionFact,
    PredictionRecord,
)


def snake(name):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def prediction_date(day):
    day = int(day)
    return PredictionDate(
        day,
        (day - 1) // 112 + 1,
        ("spring", "summer", "fall", "winter")[((day - 1) // 28) % 4],
        (day - 1) % 28 + 1,
    )


def item_identities(data):
    result = {}
    ambiguous = set()
    for table, prefix in (("objects", "O"), ("shirts", "S"), ("furniture", "F")):
        for key, value in data.catalogs["predictor_" + table].items():
            if isinstance(value, Mapping):
                name, identifier = (
                    value.get("name"),
                    value.get("id", key.removeprefix("_")),
                )
                if name:
                    qualified = f"({prefix}){identifier}"
                    if name in result and result[name] != qualified:
                        ambiguous.add(name)
                    else:
                        result[name] = qualified
    for table, prefix in (("weapons", "W"), ("boots", "B")):
        for key, name in data.catalogs["predictor_" + table].items():
            if isinstance(name, str) and name not in result:
                result[name] = f"({prefix}){key}"
    return {
        name: identifier for name, identifier in result.items() if name not in ambiguous
    }


def product_id(name, identities):
    if name in identities:
        return identities[name]
    if name.startswith("Smoked "):
        return "(O)SmokedFish"
    if name.startswith("Pickled "):
        return "(O)342"
    if name.endswith(" Juice"):
        return "(O)350"
    if name.endswith(" Jelly"):
        return "(O)344"
    if name.startswith("Dried "):
        return (
            "(O)DriedMushrooms"
            if "Mushroom" in name or name in ("Dried Morel", "Dried Chanterelle")
            else "(O)DriedFruit"
        )
    return None


@dataclass(frozen=True, slots=True)
class RecordContext:
    player_ids: tuple[int | None, ...]
    player_index: int
    player_scoped: bool
    calculation_offset: int
    community_center_complete: bool
    geodes_cracked: tuple[int, ...] = ()
    mystery_boxes_opened: tuple[int, ...] = ()
    town_key_holders: tuple[int | None, ...] = ()

    @classmethod
    def from_prediction(cls, context):
        return cls(
            tuple(context.save["mp_ids"]),
            context.player_index,
            context.player_scoped,
            context.save.get("_calculation_offset", 0),
            context.save.get("anyCcComplete", context.save["ccComplete"]),
            tuple(context.save.get("geodesCracked", ())),
            tuple(context.save.get("mysteryBoxesOpened", ())),
            tuple(context.save.get("townKeyHolders", ())),
        )


@dataclass(slots=True)
class RecordDraft:
    section: str
    facts: dict[str, Any]
    day: int | None = None
    sequence: int | None = None
    player_id: int | None = None
    location: str | None = None
    item: Any = None
    quantity: Any = None
    price: Any = None
    alternatives: list[PredictionAlternative] = field(default_factory=list)


def new_draft(section, raw, context):
    draft = RecordDraft(section, dict(raw))
    draft.day = draft.facts.get("day")
    draft.sequence = next(
        (
            draft.facts[k]
            for k in (
                "numCracked",
                "numOpened",
                "timesEnchanted",
                "tableRow",
                "numPlayed",
            )
            if draft.facts.get(k) is not None
        ),
        None,
    )
    player_index = draft.facts.get(
        "whichPlayer",
        draft.facts.get(
            "player", context.player_index if context.player_scoped else None
        ),
    )
    draft.player_id = (
        context.player_ids[int(player_index)]
        if player_index is not None and 0 <= int(player_index) < len(context.player_ids)
        else None
    )
    draft.location, draft.item, draft.quantity, draft.price, draft.alternatives = (
        None,
        draft.facts.get("item"),
        draft.facts.get("qty", draft.facts.get("itemQty")),
        draft.facts.get("price"),
        [],
    )
    if isinstance(draft.item, Mapping):
        draft.facts["item_id"] = draft.item.get("item_id")
        draft.item, draft.quantity, draft.price = (
            draft.item.get("name"),
            draft.item.get("qty", draft.quantity),
            draft.item.get("price", draft.price),
        )
    return draft


def finish_draft(draft, identities):
    section = draft.section
    time = (
        int(draft.facts["trainTime"])
        if section == "train" and draft.facts.get("arrives")
        else None
    )
    if section == "trash" and isinstance(draft.item, str):
        match = re.fullmatch("(.*) x(\\d+)", draft.item)
        if match:
            draft.item, draft.quantity = (match[1], int(match[2]))
    if isinstance(draft.price, str) and draft.price.endswith("g"):
        draft.price = int(draft.price[:-1].replace(",", ""))
    if isinstance(draft.item, str) and " or " in draft.item:
        choices = draft.item.split(" or ")
        draft.item = choices[0]
        draft.alternatives.extend(
            (
                PredictionAlternative(
                    "Session RNG or save-dependent alternative",
                    identities.get(name),
                    name,
                    draft.quantity if isinstance(draft.quantity, int) else None,
                )
                for name in choices[1:]
            )
        )
    if isinstance(draft.item, str) and draft.item.endswith(" or Qi Bean (1 or 5)"):
        draft.item = draft.item.removesuffix(" or Qi Bean (1 or 5)")
    return PredictionRecord(
        date=prediction_date(draft.day) if draft.day is not None else None,
        sequence=int(draft.sequence) if draft.sequence is not None else None,
        player_id=draft.player_id,
        location=draft.location,
        time=time,
        item_id=draft.facts.get("item_id")
        or (
            "(O)390"
            if draft.item == "Stone" and section in ("geode", "mystery")
            else identities.get(draft.item)
        )
        if isinstance(draft.item, str)
        else None,
        item_name=draft.item if isinstance(draft.item, str) else None,
        quantity=int(draft.quantity)
        if isinstance(draft.quantity, (int, float))
        else None,
        price=int(draft.price) if isinstance(draft.price, (int, float)) else None,
        alternatives=tuple(draft.alternatives),
        facts=tuple(
            (
                PredictionFact(snake(key), rules.immutable_fact(value))
                for key, value in draft.facts.items()
            )
        ),
    )
