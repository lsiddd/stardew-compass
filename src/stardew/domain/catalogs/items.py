from dataclasses import dataclass
from collections.abc import Mapping


@dataclass(frozen=True, slots=True)
class ItemCatalog:
    objects: Mapping[str, str]
    big_craftables: Mapping[str, str]

    def name(self, item_id, *, kind="Object", big_craftable=False, fallback=None):
        identifier = item_id or ""
        if identifier.startswith("(BC)") or big_craftable:
            names = self.big_craftables
        elif identifier.startswith("(O)") or kind in (
            "Item",
            "Object",
            "ColoredObject",
        ):
            names = self.objects
        else:
            names = {}
        key = identifier.split(")", 1)[-1] if identifier.startswith("(") else identifier
        return names.get(key, fallback or ("#" + identifier if identifier else kind))
