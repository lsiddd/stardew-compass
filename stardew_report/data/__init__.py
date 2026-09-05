"""Versioned upstream data, loaded once and copied when rules mutate it."""

import json
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=4)
def load_data(name):
    return json.loads(
        Path(__file__).with_name(name + ".json").read_text(encoding="utf-8")
    )


def load_table(name, index):
    return load_data(name)[index]
