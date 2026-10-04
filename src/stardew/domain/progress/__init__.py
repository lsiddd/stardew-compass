"""Native, presentation-independent progress analysis for all 27 sections."""

from collections.abc import Sequence

from stardew.domain.models.state import GameState
from stardew.domain.models.game_data import GameData

from . import collections, completion, player, world
from .common import Context
from .models import (
    ProgressFact,
    ProgressItem,
    ProgressMetric,
    ProgressResult,
    PlayerProgress,
)

PROGRESS_SECTIONS = (
    "summary",
    "money",
    "skills",
    "skill_mastery",
    "quests",
    "special_orders",
    "monsters",
    "stardrops",
    "family",
    "social",
    "cooking",
    "crafting",
    "fishing",
    "basic_shipping",
    "crop_shipping",
    "powers",
    "museum",
    "secret_notes",
    "journal_scraps",
    "bundles",
    "raccoons",
    "grandpa",
    "walnuts",
    "island_upgrades",
    "perfection_tracker",
    "arcade_games",
    "animals",
)

RULES = {
    "summary": world.summary,
    "money": world.money,
    "skills": player.skills,
    "skill_mastery": lambda ctx: player.skills(ctx, mastery=True),
    "quests": player.quests,
    "special_orders": world.special_orders,
    "monsters": player.monsters,
    "stardrops": player.stardrops,
    "family": player.family,
    "social": player.social,
    "cooking": lambda ctx: collections.recipes(ctx, cooking=True),
    "crafting": lambda ctx: collections.recipes(ctx, cooking=False),
    "fishing": collections.fishing,
    "basic_shipping": collections.shipping,
    "crop_shipping": lambda ctx: collections.shipping(ctx, crops=True),
    "powers": player.powers,
    "museum": collections.museum,
    "secret_notes": world.notes,
    "journal_scraps": lambda ctx: world.notes(ctx, journal=True),
    "bundles": world.bundles,
    "raccoons": world.raccoons,
    "grandpa": completion.grandpa,
    "walnuts": world.walnuts,
    "island_upgrades": world.island_upgrades,
    "perfection_tracker": completion.perfection,
    "arcade_games": player.arcade,
    "animals": world.animals,
}

MINIMUM_VERSIONS = {
    "skill_mastery": (1, 6, 0),
    "special_orders": (1, 5, 0),
    "powers": (1, 6, 0),
    "secret_notes": (1, 3, 0),
    "journal_scraps": (1, 5, 0),
    "raccoons": (1, 6, 0),
    "walnuts": (1, 5, 0),
    "island_upgrades": (1, 5, 0),
    "perfection_tracker": (1, 5, 0),
    "arcade_games": (1, 5, 0),
    "animals": (1, 6, 0),
}

SECTION_DEPENDENCIES = {
    "perfection_tracker": (
        "skills",
        "monsters",
        "stardrops",
        "social",
        "cooking",
        "crafting",
        "fishing",
        "basic_shipping",
        "walnuts",
    ),
}


def analyze_progress(
    state: GameState, data: GameData, sections: Sequence[str] | None = None
) -> tuple[ProgressResult, ...]:
    """Analyze one immutable game snapshot, computing prerequisites before filtering.

    A fresh context per call prevents stale multiplayer or perfection state. Caller
    order only controls returned order; it cannot alter computed category values.
    """
    selected = PROGRESS_SECTIONS if sections is None else tuple(sections)
    invalid = set(selected) - set(PROGRESS_SECTIONS)
    if invalid:
        raise ValueError("Unknown progress section(s): " + ", ".join(sorted(invalid)))
    required = set(selected)
    pending = list(selected)
    while pending:
        for dependency in SECTION_DEPENDENCIES.get(pending.pop(), ()):
            if dependency not in required:
                required.add(dependency)
                pending.append(dependency)
    if not required:
        return ()
    ctx = Context(state, data)
    results = {}
    for section in PROGRESS_SECTIONS:
        if section not in required:
            continue
        minimum = MINIMUM_VERSIONS.get(section, (1, 2, 0))
        if ctx.version < minimum:
            required_version = ".".join(str(part) for part in minimum)
            results[section] = ProgressResult(
                section,
                section.replace("_", " ").title(),
                available=False,
                diagnostics=(f"Requires game version {required_version} or later.",),
            )
        else:
            results[section] = RULES[section](ctx)
    return tuple(results[section] for section in selected)


__all__ = [
    "analyze_progress",
    "PROGRESS_SECTIONS",
    "ProgressResult",
    "PlayerProgress",
    "ProgressMetric",
    "ProgressItem",
    "ProgressFact",
]
