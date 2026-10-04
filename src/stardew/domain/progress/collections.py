"""Collections, recipes, shipping, and museum progress (MouseyPounds rules, MIT)."""

from .common import counts, dictionary, integer, item_id, number, value
from .models import ProgressItem, ProgressResult, facts, metric


def recipes(ctx, cooking):
    section = "cooking" if cooking else "crafting"
    catalog = ctx.updated_catalog(
        "cooking_recipes" if cooking else "crafting_recipes",
        "cooking" if cooking else "crafting",
    )
    catalog = catalog if cooking else {name: name for name in catalog}
    aliases = (
        ctx.catalog("cooking_aliases")
        if cooking
        else {"Oil Of Garlic": "Oil of Garlic"}
    )
    reverse = {name: key for key, name in catalog.items()}
    players = []
    for player in ctx.players:
        node = player.snapshot
        raw = counts(node, section + "Recipes")
        known = {
            aliases.get(name, name): num
            for name, num in raw.items()
            if name != "Wedding Ring" or cooking
        }
        base_known = {name: num for name, num in known.items() if name in reverse}
        mods = {name: num for name, num in known.items() if name not in reverse}
        crafted_raw = (
            counts(node, "recipesCooked")
            if cooking
            else {reverse[name]: num for name, num in base_known.items()}
        )
        crafted = {
            key: num for key, num in crafted_raw.items() if num > 0 and key in catalog
        }
        mod_crafted = (
            sum(num > 0 for key, num in crafted_raw.items() if key not in catalog)
            if cooking
            else sum(num > 0 for num in mods.values())
        )
        missing = [
            ProgressItem(
                str(key),
                name,
                crafted_raw.get(key, 0),
                1,
                1,
                "unknown_recipe" if name not in base_known else "known_recipe",
            )
            for key, name in catalog.items()
            if key not in crafted
        ]
        prefix = ("cook", "Cook") if cooking else ("craft", "Craft")
        milestones = (
            (("cook", "Cook", 10), ("sous_chef", "Sous Chef", 25))
            if cooking
            else (("diy", "D.I.Y.", 15), ("artisan", "Artisan", 30))
        )
        all_count = len(crafted) + mod_crafted
        metrics = [
            metric(
                section,
                section.title(),
                len(crafted),
                len(catalog),
                (x.item_id for x in missing),
            )
        ]
        metrics.extend(
            metric(key, name, all_count, goal) for key, name, goal in milestones
        )
        metrics.append(
            metric(
                "gourmet_chef" if cooking else "craft_master",
                "Gourmet Chef" if cooking else "Craft Master",
                all_count,
                len(catalog) + len(mods),
            )
        )
        key = ctx.player_id(player)
        ctx.perfection[key][section] = (len(crafted), len(catalog))
        players.append(
            ctx.player_result(
                player,
                metrics,
                missing,
                facts(
                    known_recipes=len(base_known),
                    mod_known=len(mods),
                    mod_crafted=mod_crafted,
                ),
            )
        )
    return ProgressResult(section, section.title(), players=tuple(players))


def fishing(ctx):
    catalog = ctx.updated_catalog("fish", "fishing")
    ignore = set(ctx.catalog("non_fish"))
    extras = {
        "898": "Son of Crimsonfish",
        "899": "Ms. Angler",
        "900": "Legend II",
        "901": "Radioactive Carp",
        "902": "Glacierfish Jr.",
    }
    if ctx.version < (1, 6, 0):
        ignore |= {"372", *extras}
    players = []
    for player in ctx.players:
        raw = {}
        for entry in player.snapshot.findall("fishCaught/item"):
            raw[item_id(value(entry, "key/*", ""))] = integer(
                entry, "value/ArrayOfInt/int"
            )
        caught = {key: count for key, count in raw.items() if count > 0}
        base = {
            key: count
            for key, count in caught.items()
            if key in catalog and key not in ignore
        }
        mods = {
            key: count
            for key, count in caught.items()
            if key not in catalog and key not in extras and key not in ignore
        }
        total = sum(count for key, count in caught.items() if key not in ignore)
        missing = tuple(
            ProgressItem(key, name, 0, 1, 1, "fish")
            for key, name in catalog.items()
            if key not in base
        )
        goals = [
            ("fisherman", "Fisherman", len(base), 10),
            ("ol_mariner", "Ol' Mariner", len(base), 24),
            ("mother_catch", "Mother Catch", total, 100),
            (
                "master_angler",
                "Master Angler",
                len(base),
                len(catalog) if ctx.version >= (1, 4, 0) else min(59, len(catalog)),
            ),
        ]
        metrics = [
            metric(
                "fishing",
                "Fish collection",
                len(base),
                len(catalog),
                (x.item_id for x in missing),
            )
        ]
        metrics.extend(metric(*goal) for goal in goals)
        bobbers = min(39, 1 + len(caught) // 2)
        if ctx.version >= (1, 6, 0):
            metrics.append(metric("bobber_styles", "Bobber styles", bobbers, 39))
        ctx.perfection[ctx.player_id(player)]["fishing"] = (len(base), len(catalog))
        players.append(
            ctx.player_result(
                player,
                metrics,
                missing,
                facts(
                    total_catches=total,
                    mod_fish=len(mods),
                    unique_catches=len(caught),
                    bobber_fish_remaining=max(0, 76 - len(caught)),
                    bobber_alternatives=tuple(
                        key for key in extras if key not in caught
                    ),
                ),
            )
        )
    return ProgressResult("fishing", "Fishing", players=tuple(players))


def shipping(ctx, crops=False):
    catalog = (
        ctx.catalog("crops") if crops else ctx.updated_catalog("shipping", "shipping")
    )
    extra = {
        "454": "Ancient Fruit",
        "591": "Tulip",
        "593": "Summer Spangle",
        "595": "Fairy Rose",
        "597": "Blue Jazz",
    }
    players = []
    for player in ctx.players:
        raw = counts(player.snapshot, "basicShipped")
        target = 15 if crops else 1
        done = sum(raw.get(key, 0) >= target for key in catalog)
        missing = tuple(
            ProgressItem(
                key,
                name,
                raw.get(key, 0),
                target,
                target - raw.get(key, 0),
                "crop" if crops else "shipping",
            )
            for key, name in catalog.items()
            if raw.get(key, 0) < target
        )
        if crops:
            pool = {**catalog, **extra}
            max_key = max(pool, key=lambda key: raw.get(key, 0), default="")
            max_count = raw.get(max_key, 0)
            metrics = (
                metric(
                    "polyculture",
                    "Polyculture",
                    done,
                    len(catalog),
                    (x.item_id for x in missing),
                ),
                metric("monoculture", "Monoculture", max_count, 300),
            )
            detail = facts(
                most_shipped_crop=max_key if max_count else None,
                most_shipped_count=max_count,
            )
        else:
            metrics = (
                metric(
                    "shipping",
                    "Full Shipment",
                    done,
                    len(catalog),
                    (x.item_id for x in missing),
                ),
            )
            detail = ()
            ctx.perfection[ctx.player_id(player)]["shipping"] = (done, len(catalog))
        players.append(ctx.player_result(player, metrics, missing, detail))
    return ProgressResult(
        "crop_shipping" if crops else "basic_shipping",
        "Crop Shipping" if crops else "Basic Shipping",
        players=tuple(players),
    )


def museum(ctx):
    artifacts, minerals = ctx.catalog("artifacts"), ctx.catalog("minerals")
    all_items = {**artifacts, **minerals}
    donated = set()
    for location in ctx.locations("LibraryMuseum"):
        donated.update(
            value(entry, "value/*", "")
            for entry in location.findall("museumPieces/item")
            if value(entry, "value/*", "") in all_items
        )
    missing = tuple(
        ProgressItem(key, name, 0, 1, 1, "artifact" if key in artifacts else "mineral")
        for key, name in all_items.items()
        if key not in donated
    )
    players = []
    for player in ctx.players:
        raw_artifacts = {
            value(entry, "key/*", "")
            for entry in player.snapshot.findall("archaeologyFound/item")
            if integer(entry, "value/ArrayOfInt/int") > 0
        }
        raw_minerals = {
            key
            for key, count in counts(player.snapshot, "mineralsFound").items()
            if count > 0
        }
        found_artifacts = raw_artifacts & set(artifacts)
        found_minerals = raw_minerals & set(minerals)
        found = found_artifacts | found_minerals
        items = tuple(
            ProgressItem(
                key, name, 0, 1, 1, "artifact" if key in artifacts else "mineral"
            )
            for key, name in all_items.items()
            if key not in found
        )
        players.append(
            ctx.player_result(
                player,
                (
                    metric(
                        "artifacts_found",
                        "Artifacts found",
                        len(found_artifacts),
                        len(artifacts),
                    ),
                    metric(
                        "minerals_found",
                        "Minerals found",
                        len(found_minerals),
                        len(minerals),
                    ),
                ),
                items,
                facts(
                    found_not_donated=tuple(
                        key for key in all_items if key in found and key not in donated
                    ),
                    donated_not_found=tuple(
                        key for key in all_items if key in donated and key not in found
                    ),
                ),
            )
        )
    return ProgressResult(
        "museum",
        "Museum Collection",
        (
            metric("treasure_trove", "Treasure Trove", len(donated), 40),
            metric(
                "rusty_key_donations",
                "Donate enough items to get the Rusty Key",
                len(donated),
                60,
            ),
            metric(
                "complete_collection",
                "A Complete Collection",
                len(donated),
                len(all_items),
                (x.item_id for x in missing),
            ),
        ),
        tuple(players),
        missing,
    )
