"""Build records at emission time without retaining mutable algorithm locals."""

from .calendar import build_night, build_statue, build_train, build_trash
from .common import finish_draft, item_identities, new_draft
from .events import build_gembirds, build_makeover, build_winterstar
from .loot import build_enchant, build_geode, build_prize, build_raccoon
from .shops import build_book, build_cart, build_krobus, build_sandy, build_wallpaper

__all__ = ["build_records", "item_identities"]

BUILDERS = {
    "geode": build_geode,
    "mystery": build_geode,
    "raccoon": build_raccoon,
    "enchant": build_enchant,
    "prize": build_prize,
    "trash": build_trash,
    "train": build_train,
    "night": build_night,
    "crane": build_night,
    "statue": build_statue,
    "krobus": build_krobus,
    "cart": build_cart,
    "sandy": build_sandy,
    "wallpaper": build_wallpaper,
    "book": build_book,
    "gembirds": build_gembirds,
    "makeover": build_makeover,
    "winterstar": build_winterstar,
}


def build_records(section, raw, context, identities):
    draft = new_draft(section, raw, context)
    builder = BUILDERS.get(section)
    records = builder(draft, context, identities) if builder else None
    return tuple(records) if records is not None else (finish_draft(draft, identities),)
