"""Save snapshot access shared by native progress rules."""

from __future__ import annotations
import re
from .catalogs import CATALOG_ADDITIONS
from .models import PlayerProgress


def version(value):
    return tuple(
        int(x) for x in (re.findall(r"\d+", value or "1.2")[:3] + ["0"] * 3)[:3]
    )


def number(value, default=0):
    if value is None or value == "":
        return default
    try:
        parsed = float(value)
        return int(parsed) if parsed.is_integer() else parsed
    except (TypeError, ValueError):
        return default


def value(node, path, default=None):
    found = node.find(path) if node is not None else None
    return found.text(default) if found is not None else default


def integer(node, path, default=0):
    return number(value(node, path), default)


def values(node, path):
    return (
        tuple(item.text("") for item in node.findall(path)) if node is not None else ()
    )


def dictionary(node, path):
    result = {}
    if node is None:
        return result
    for item in node.findall(path + "/item"):
        result[value(item, "key/*", "")] = value(item, "value/*", "")
    return result


def counts(node, path):
    return {key: number(val) for key, val in dictionary(node, path).items()}


def item_id(raw):
    return raw.split(")", 1)[-1] if raw.startswith("(") else raw


def object_type(node):
    for key, val in node.attributes.items():
        if key == "type" or key.endswith("}type") or key.endswith(":type"):
            return val
    return node.tag


class Context:
    """Analysis-local data; never writes to the immutable game state or catalog."""

    def __init__(self, state, data):
        self.state = state
        self.root = state.snapshot
        self.players = state.players
        self.version = version(state.rules_version)
        self.data = data
        self.mail = {}
        self.events = {}
        self.stats = {}
        self.perfection = {}
        for index, player in enumerate(self.players):
            key = self.player_id(player, index)
            self.mail[key] = set(player.mail)
            self.events[key] = set(player.events)
            if self.version >= (1, 3, 0):
                stats = dict(player.stats)
            else:
                old = self.root.find("stats")
                stats = {}
                for child in old.children if old is not None else ():
                    if child.content is not None and not child.children:
                        try:
                            stats[child.tag] = int(child.content)
                        except ValueError:
                            continue
            self.stats[key] = stats
            self.perfection[key] = {}
        self.host_id = self.player_id(self.players[0])
        self.partners = {}
        for item in self.root.findall("farmerFriendships/item"):
            friends = values(item, "key/FarmerPair/*")
            if (
                len(friends) >= 2
                and value(item, "value/Friendship/Status") == "Married"
            ):
                self.partners[friends[0]] = friends[1]
                self.partners[friends[1]] = friends[0]

    def player_id(self, player, index=0):
        if self.version < (1, 3, 0):
            return "0"
        if player.player_id is not None:
            return str(player.player_id)
        position = next(
            (i for i, candidate in enumerate(self.players) if candidate is player),
            index,
        )
        return "player_" + str(position)

    def catalog(self, name):
        return self.data.catalogs["checkup_" + name]

    def updated_catalog(self, name, rule):
        catalog = self.catalog(name)
        result = (
            {str(k): v for k, v in catalog.items()}
            if hasattr(catalog, "items")
            else list(catalog)
        )
        if name == "friendship_events":
            result = {
                key: [tuple(event) for event in events]
                for key, events in result.items()
            }
        for ver, additions in CATALOG_ADDITIONS.get(rule, {}).items():
            if self.version < version(ver):
                continue
            for operation, path, addition in additions:
                if operation == "set":
                    result[path[-1]] = addition
                elif len(path) == 1:
                    result.extend(addition)
                else:
                    result.setdefault(path[-1], []).extend(addition)
        return result

    def locations(self, kind=None):
        return tuple(
            n
            for n in self.root.findall("locations/GameLocation")
            if kind is None or object_type(n) == kind or value(n, "name") == kind
        )

    def player_result(self, player, metrics=(), items=(), detail=()):
        return PlayerProgress(
            self.player_id(player),
            player.name,
            tuple(metrics),
            tuple(items),
            tuple(detail),
        )
