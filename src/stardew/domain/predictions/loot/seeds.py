"""Seed construction shared by geodes and mystery boxes."""

from collections.abc import Mapping
from typing import Any
from ..report_support import int32, random_seed


def player_sequence_seed(save: Mapping[str, Any], sequence: int, player: int) -> int:
    players = save.get("mp_ids")
    player_part = int32(players[player]) / 2 if players is not None else 0
    return random_seed(
        sequence, save["gameID"] / 2, player_part, legacy=save["useLegacyRandom"]
    )
