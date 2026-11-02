"""One declaration of prediction identity, scope, ranges and prerequisites."""

from dataclasses import dataclass
from typing import Callable, Literal

from . import report_rules as rules

Scope = Literal["world", "player", "mixed"]
RangeKind = Literal["days", "sequence", "years", "games", "fixed"]


@dataclass(frozen=True, slots=True)
class Feature:
    identifier: str
    title: str
    calculate: Callable
    scope: Scope = "world"
    range_kind: RangeKind = "days"
    page_size: int = 28
    minimum: str | None = None
    player_id_since: str | None = None
    counter: str | None = None


FEATURES = (
    Feature("mines", "Mines", rules.predict_mines),
    Feature("cart", "Traveling Cart", rules.predict_cart, page_size=7),
    Feature(
        "geode",
        "Geodes",
        rules.predict_geodes,
        "player",
        "sequence",
        20,
        player_id_since="1.6",
        counter="geodesCracked",
    ),
    Feature(
        "mystery",
        "Mystery Boxes",
        rules.predict_mystery_boxes,
        "player",
        "sequence",
        20,
        "1.6",
        "1.6",
        "mysteryBoxesOpened",
    ),
    Feature("train", "Trains", rules.predict_trains),
    Feature("night", "Night Events", rules.predict_night),
    Feature("crane", "Crane Game", rules.predict_crane, minimum="1.4"),
    Feature("krobus", "Krobus", rules.predict_krobus, page_size=7),
    Feature("sandy", "Sandy", rules.predict_sandy, page_size=7),
    Feature("wallpaper", "Wallpaper", rules.predict_wallpaper, page_size=7),
    Feature("trash", "Garbage Cans", rules.predict_trash, scope="player"),
    Feature(
        "enchant",
        "Enchantments",
        rules.predict_enchantments,
        "player",
        "sequence",
        20,
        "1.5",
        "1.6",
        "timesEnchanted",
    ),
    Feature(
        "minechest",
        "Mine Chests",
        rules.predict_mine_chests,
        range_kind="fixed",
        minimum="1.5",
    ),
    Feature(
        "gembirds",
        "Gem Birds",
        rules.predict_gem_birds,
        range_kind="fixed",
        minimum="1.5",
    ),
    Feature(
        "winterstar",
        "Winter Star",
        rules.predict_winter_star,
        "mixed",
        "years",
        1,
        player_id_since="1.3",
    ),
    Feature(
        "makeover",
        "Desert Festival",
        rules.predict_makeover,
        "mixed",
        "years",
        1,
        "1.6",
        "1.6",
    ),
    Feature("greenrain", "Weather", rules.predict_green_rain, minimum="1.6"),
    Feature(
        "cj",
        "Calico Jack",
        rules.predict_calico_jack,
        scope="player",
        range_kind="games",
        page_size=20,
    ),
    Feature("book", "Bookseller", rules.predict_bookseller, minimum="1.6"),
    Feature(
        "statue",
        "Statue Blessings",
        rules.predict_statues,
        scope="mixed",
        minimum="1.6",
        player_id_since="1.6",
    ),
    Feature(
        "prize",
        "Prize Tickets",
        rules.predict_prize_ticket,
        "player",
        "sequence",
        20,
        "1.6",
        "1.6",
        "ticketPrizesClaimed",
    ),
    Feature(
        "raccoon",
        "Raccoon Requests",
        rules.predict_raccoon,
        "world",
        "sequence",
        10,
        "1.6",
        counter="timesFedRaccoons",
    ),
)
REGISTRY = {feature.identifier: feature for feature in FEATURES}
SECTION_IDS = tuple(REGISTRY)


@dataclass(frozen=True, slots=True)
class Window:
    """Half-open interval in the unit declared by the feature."""

    start: int
    stop: int

    def contains(self, value: int) -> bool:
        return self.start <= value < self.stop


def day_window(
    feature: Feature, saved_day: int | None, start: int | None, count: int | None
) -> Window | None:
    if feature.range_kind != "days":
        return None
    first = start if start is not None else saved_day
    if first is None:
        raise ValueError(
            "A calendar prediction requires a start day or saved days_played"
        )
    return Window(first, first + (count or feature.page_size))
