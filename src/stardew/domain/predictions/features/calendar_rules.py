"""Shared date and seed rules for calendar predictions."""

from ..report_support import SystemRandom, random_seed, trunc_div

# The installed DLL profile is selected only from verified game-data provenance.
# Its train rule must not be inferred from the save's version string alone.
INSTALLED_GAME_PROFILE = "installed-f3e97f01"
FESTIVAL_DAYS = frozenset((13, 24, 39, 56, 72, 83, 92, 109))
# Only Night Market replaces a map in the Valley context. Trout Derby and
# SquidFest have no map replacements, so they do not force sunny weather.
PASSIVE_VALLEY_FESTIVAL_DAYS = frozenset((99, 100, 101))


def calendar_parts(day):
    """Return year, zero-based season and one-based day of month."""
    return (day - 1) // 112 + 1, (day - 1) // 28 % 4, (day - 1) % 28 + 1


def is_festival(day):
    return (day - 1) % 112 + 1 in FESTIVAL_DAYS


def day_random(save, day, *extra):
    """Utility.CreateDaySaveRandom: integer division happens before doubles."""
    return SystemRandom(
        random_seed(
            day,
            trunc_div(save["gameID"], 2),
            *extra,
            legacy=save["useLegacyRandom"],
        )
    )
