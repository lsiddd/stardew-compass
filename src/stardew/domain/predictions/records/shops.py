"""Feature-local conversion of calculated facts to public prediction records."""

from ..features.calendar_rules import is_festival
from ..report_models import PredictionFact, PredictionRecord
from .common import prediction_date as _date
from .common import snake as _snake


def build_krobus(draft, context, identities):
    column = int(draft.facts["i"])
    draft.day = context.calculation_offset + (3, 6)[column]
    draft.item, draft.quantity, draft.price = (
        draft.facts["item"][column],
        draft.facts["qty"][column],
        draft.facts["price"][column],
    )
    draft.facts["item_id"] = draft.facts.get("itemIDs", [None, None])[column]


def build_cart(draft, context, identities):
    if isinstance(draft.item, (list, tuple)):
        draft.item, draft.quantity, draft.price = draft.item
        draft.day = draft.facts.get("startDay")


def build_sandy(draft, context, identities):
    draft.item = draft.item.split(" ID:")[0]
    draft.facts["item_id"] = f"(S){draft.facts['numID']}"


def build_wallpaper(draft, context, identities):
    result = []
    day = int(draft.day)
    wednesday = (day - 1) % 7 == 2
    festival_closed = is_festival(day) and (day - 1) % 112 + 1 not in (56, 83)
    for location, wall, flooring, equivalent, available in (
        (
            "Pierre",
            draft.facts["wp_p"],
            draft.facts["fl_p"],
            draft.facts["eq_p"],
            not festival_closed
            and (
                context.community_center_complete
                or not wednesday
                or bool(context.town_key_holders)
            ),
        ),
        (
            "JojaMart",
            draft.facts["wp_j"],
            draft.facts["fl_j"],
            draft.facts["eq_j"],
            not festival_closed and not context.community_center_complete,
        ),
    ):
        if not available:
            result.append(
                PredictionRecord(
                    date=_date(draft.day),
                    location=location,
                    facts=(
                        PredictionFact("open", False),
                        PredictionFact(
                            "reason",
                            "Stores closed for daytime festival"
                            if festival_closed
                            else "JojaMart replaced after Community Center ceremony"
                            if location == "JojaMart"
                            else "Wednesday before Community Center ceremony; no saved Key To The Town",
                        ),
                    ),
                )
            )
            continue
        for kind, number in (("Wallpaper", wall), ("Flooring", flooring)):
            result.append(
                PredictionRecord(
                    date=_date(draft.day),
                    location=location,
                    item_name=kind,
                    quantity=1,
                    facts=(
                        PredictionFact("texture_id", int(number) - 1),
                        PredictionFact("display_number", int(number)),
                        PredictionFact(
                            "equivalent_item",
                            equivalent if kind == "Wallpaper" else None,
                        ),
                        *(
                            (
                                PredictionFact(
                                    "access_condition",
                                    "Key To The Town; Pierre must be serving",
                                ),
                                PredictionFact(
                                    "town_key_holders", context.town_key_holders
                                ),
                            )
                            if location == "Pierre"
                            and wednesday
                            and not context.community_center_complete
                            else ()
                        ),
                    ),
                )
            )
    return result


def build_book(draft, context, identities):
    result = []
    for index, visit in enumerate(draft.facts["days"]):
        for slot, stock in draft.facts["stock"][str(index)].items():
            if stock:
                name, cost = (stock["name"], stock["price"])
                result.append(
                    PredictionRecord(
                        date=_date(context.calculation_offset + visit),
                        item_id=identities.get(name),
                        item_name=name,
                        quantity=1,
                        price=cost,
                        facts=(PredictionFact("slot", _snake(slot)),),
                    )
                )
    return result
