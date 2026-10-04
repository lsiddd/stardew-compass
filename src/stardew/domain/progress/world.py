"""World quests, notes, walnuts, community development and island upgrades."""

from .common import counts, dictionary, integer, number, object_type, value, values
from .models import ProgressItem, ProgressResult, facts, metric


def summary(ctx):
    player, metadata = ctx.players[0], ctx.state.metadata
    farm_types = {
        "0": "Standard",
        "1": "Riverland",
        "2": "Forest",
        "3": "Hill-top",
        "4": "Wilderness",
        "5": "Four Corners",
        "6": "Beach",
        "7": "Meadowlands",
        "MeadowlandsFarm": "Meadowlands",
    }
    return ProgressResult(
        "summary",
        "Summary",
        facts=facts(
            farm_name=player.farm_name or "",
            farm_type=farm_types.get(str(metadata.farm_type or 0), "Unknown"),
            players=tuple(player.name for player in ctx.players),
            game_version=metadata.game_version or "1.2",
            version_label=ctx.state.world.game_version_label,
            day=metadata.day or 0,
            season=metadata.season,
            year=metadata.year or 0,
            days_played=ctx.stats[ctx.host_id].get("daysPlayed"),
            milliseconds_played=player.milliseconds_played or 0,
        ),
    )


def money(ctx):
    earned = ctx.players[0].total_money_earned or 0
    goals = (
        ("greenhorn", "Greenhorn", 15000),
        ("cowpoke", "Cowpoke", 50000),
        ("homesteader", "Homesteader", 250000),
        ("millionaire", "Millionaire", 1000000),
        ("legend", "Legend", 10000000),
    )
    separate = ctx.players[0].use_separate_wallets is True
    players = (
        tuple(
            ctx.player_result(
                player,
                detail=facts(
                    individual_money_earned=ctx.stats[ctx.player_id(player)].get(
                        "individualMoneyEarned", 0
                    )
                ),
            )
            for player in ctx.players
        )
        if separate
        else ()
    )
    return ProgressResult(
        "money",
        "Money",
        tuple(metric(key, name, earned, goal) for key, name, goal in goals),
        players,
        facts=facts(
            total_money_earned=earned,
            separate_wallets=separate,
            unexplained_earnings=earned
            - sum(
                ctx.stats[ctx.player_id(player)].get("individualMoneyEarned", 0)
                for player in ctx.players
            )
            if separate
            else None,
        ),
    )


def special_orders(ctx):
    done = set(values(ctx.root, "completedSpecialOrders/string"))
    town, qi = ctx.catalog("special_orders"), ctx.catalog("qi_orders")
    missing = tuple(
        ProgressItem(key, name, 0, 1, 1, "town_order")
        for key, name in town.items()
        if key not in done
    )
    return ProgressResult(
        "special_orders",
        "Special Orders",
        (
            metric(
                "town_special_orders",
                "Town special orders",
                len(done & set(town)),
                len(town),
                (x.item_id for x in missing),
            ),
            metric(
                "qi_special_orders", "Qi's special orders", len(done & set(qi)), len(qi)
            ),
        ),
        items=missing,
        facts=facts(completed_ids=tuple(sorted(done))),
    )


def notes(ctx, journal=False):
    players = []
    default_statues = set()
    for location in ctx.locations():
        if value(location, "name") != "Town":
            continue
        for entry in location.findall(".//item"):
            node = entry.find("value/Object")
            if (
                node is not None
                and value(node, "name") == "Stone Junimo"
                and value(entry, "key/Vector2/X") == "57"
                and value(entry, "key/Vector2/Y") == "16"
            ):
                default_statues.add(id(node))
    stone = any(
        node.tag in ("Item", "Object")
        and value(node, "name") == "Stone Junimo"
        and id(node) not in default_statues
        for node in ctx.root.iter()
    )
    for player in ctx.players:
        key, node = ctx.player_id(player), player.snapshot
        seen = {int(number(raw)) for raw in values(node, "secretNotesSeen/int")}
        flags = ctx.mail[key]
        if journal:
            note_count = 11
            ids = set(range(1001, 1012))
            rewards = {
                1004: "Island_W_BuriedTreasure",
                1006: "Island_W_BuriedTreasure2",
                1010: "Island_N_BuriedTreasure",
                1009: None,
            }
            found = {num for num, flag in rewards.items() if flag in flags}
            if "Mermaid" in values(ctx.root, "collectedNutTracker/string"):
                found.add(1009)
            mod_count = sum(num >= 1012 for num in seen)
            items = tuple(
                ProgressItem(
                    str(num), f"Journal Scrap #{num - 1000}", 0, 1, 1, "journal_scrap"
                )
                for num in sorted(ids - seen)
            )
            items += tuple(
                ProgressItem(
                    str(num),
                    f"Journal Scrap #{num - 1000} reward",
                    0,
                    1,
                    1,
                    "note_reward",
                )
                for num in sorted(set(rewards) - found)
            )
            detail = facts(
                visited_island="Visited_Island" in flags, mod_notes=mod_count
            )
        else:
            note_count = (
                27
                if ctx.version >= (1, 6, 0)
                else 25
                if ctx.version >= (1, 4, 0)
                else 23
            )
            ids = set(range(1, note_count + 1))
            rewards = set(range(13, note_count + 1)) - {24, 26, 27}
            found = {
                int(num)
                for flag, num in ctx.catalog("note_flags").items()
                if flag in flags
            }
            if "2120303" in ctx.events[key]:
                found.add(23)
            if "JojaMember" in flags:
                rewards.discard(14)
            elif stone:
                found.add(14)
            mod_count = sum(note_count < num < 1000 for num in seen)
            items = tuple(
                ProgressItem(str(num), f"Secret Note #{num}", 0, 1, 1, "secret_note")
                for num in sorted(ids - seen)
            )
            items += tuple(
                ProgressItem(
                    str(num), f"Secret Note #{num} reward", 0, 1, 1, "note_reward"
                )
                for num in sorted(rewards - found)
            )
            detail = facts(
                seen_shadow_guy="520702" in ctx.events[key],
                has_magnifying_glass="HasMagnifyingGlass" in flags
                if ctx.version >= (1, 6, 0)
                else value(node, "hasMagnifyingGlass") == "true",
                mod_notes=mod_count,
            )
        metrics = (
            metric(
                "notes_read",
                "Read all journal scraps" if journal else "Read all secret notes",
                len(seen & ids),
                note_count,
                tuple(str(num) for num in sorted(ids - seen)),
            ),
            metric(
                "note_rewards",
                "Find all note rewards",
                len(found & set(rewards)),
                len(rewards),
                tuple(str(num) for num in sorted(set(rewards) - found)),
            ),
        )
        if journal:
            metrics += (
                metric(
                    "a_distant_shore",
                    "A Distant Shore",
                    int("Visited_Island" in flags),
                    1,
                ),
            )
        players.append(ctx.player_result(player, metrics, items, detail))
    return ProgressResult(
        "journal_scraps" if journal else "secret_notes",
        "Journal Scraps" if journal else "Secret Notes",
        players=tuple(players),
    )


def walnuts(ctx):
    locations, rewards = ctx.catalog("walnut_locations"), ctx.catalog("walnut_rewards")
    catalog = {
        **locations,
        **rewards,
        "GoldenCoconut": {"num": 1, "name": "Break a Golden Coconut", "hint": ""},
    }
    collected = set(values(ctx.root, "collectedNutTracker/string"))
    limited = counts(ctx.root, "limitedNutDrops")
    found = {
        key: int(entry["num"]) for key, entry in locations.items() if key in collected
    }
    found.update(
        {
            key: min(num, rewards[key]["num"])
            for key, num in limited.items()
            if key in rewards and num > 0
        }
    )
    if value(ctx.root, "goldenCoconutCracked") == "true":
        found["GoldenCoconut"] = 1
    total = sum(entry["num"] for entry in catalog.values())
    game_count = integer(ctx.root, "goldenWalnutsFound")
    missing = tuple(
        ProgressItem(
            key,
            entry["name"],
            found.get(key, 0),
            entry["num"],
            entry["num"] - found.get(key, 0),
            "walnut",
            entry["hint"],
        )
        for key, entry in catalog.items()
        if found.get(key, 0) < entry["num"]
    )
    ctx.walnut_progress = (game_count, total)
    return ProgressResult(
        "walnuts",
        "Golden Walnuts",
        (
            metric(
                "golden_walnuts",
                "Golden Walnuts",
                game_count,
                total,
                (x.item_id for x in missing),
            ),
        ),
        items=missing,
        facts=facts(
            tracked_walnuts=sum(found.values()),
            game_walnuts=game_count,
            golden_parrot_activated=value(ctx.root, "activatedGoldenParrot") == "true",
        ),
        diagnostics=(
            f"Tracked walnuts ({sum(found.values())}) differ from game count ({game_count}).",
        )
        if sum(found.values()) != game_count
        else (),
    )


def island_upgrades(ctx):
    catalog = ctx.catalog("island_upgrades")
    bought = set(catalog) & ctx.mail[ctx.host_id]
    missing = tuple(
        ProgressItem(
            key,
            entry["name"],
            0,
            1,
            1,
            "island_upgrade",
            cost=entry["cost"],
            cost_unit="walnuts",
        )
        for key, entry in catalog.items()
        if key not in bought
    )
    return ProgressResult(
        "island_upgrades",
        "Island Upgrades",
        (
            metric(
                "island_upgrades",
                "Island upgrades",
                len(bought),
                len(catalog),
                (x.item_id for x in missing),
            ),
        ),
        items=missing,
        facts=facts(
            walnut_cost_remaining=sum(
                entry["cost"] for key, entry in catalog.items() if key not in bought
            )
        ),
    )


def bundles(ctx):
    cc_mail = {
        "ccBoilerRoom": 3,
        "ccCraftsRoom": 1,
        "ccPantry": 0,
        "ccFishTank": 2,
        "ccVault": 4,
        "ccBulletin": 5,
    }
    joja_mail = {
        "jojaBoilerRoom": 3,
        "jojaCraftsRoom": 1,
        "jojaPantry": 0,
        "jojaFishTank": 2,
        "jojaVault": 4,
    }
    room_ids = {
        "Pantry": 0,
        "Crafts Room": 1,
        "Fish Tank": 2,
        "Boiler Room": 3,
        "Vault": 4,
        "Bulletin Board": 5,
        "Abandoned Joja Mart": 6,
    }
    room_names = {index: name for name, index in room_ids.items()}
    completed = set()
    entries = {}
    for location in ctx.locations("CommunityCenter"):
        completed.update(
            index
            for index, flag in enumerate(values(location, "areasComplete/boolean"))
            if flag == "true"
        )
        for item in location.findall("bundles/item"):
            key = value(item, "key/int", "")
            entries[key] = tuple(
                flag == "true"
                for flag in values(item, "value/ArrayOfBoolean/boolean")
                or values(item, "ArrayOfBoolean/boolean")
            )
    cc_count = len(completed)
    flags = ctx.mail[ctx.host_id]
    joja = "JojaMember" in flags
    joja_done = {room for flag, room in joja_mail.items() if flag in flags}
    completed |= joja_done
    event = "502261" if joja else "191393"
    ceremony = event in ctx.events[ctx.host_id]
    raw = (
        dict(ctx.catalog("bundles"))
        if ctx.version < (1, 5, 0)
        else dictionary(ctx.root, "bundleData")
    )
    items = []
    metrics = []
    for key, record in raw.items():
        fields = record.split("/")
        room, bundle_id = key.split("/", 1)
        if len(fields) < 3:
            continue
        pool = fields[2].split()
        quantity = (
            int(number(fields[4])) if len(fields) > 4 and fields[4] else len(pool) // 3
        )
        accepted = entries.get(bundle_id, ())
        done = sum(accepted)
        missing = []
        for index in range(0, len(pool) - 2, 3):
            item, qty, quality = pool[index : index + 3]
            if index // 3 < len(accepted) and accepted[index // 3]:
                continue
            missing.append(item)
            if (
                room_ids.get(room) not in completed
                and room_ids.get(room, 6) < 6
                and done < quantity
            ):
                items.append(
                    ProgressItem(
                        item,
                        ctx.catalog("object_names").get(item, item)
                        if item != "-1"
                        else "Gold",
                        0,
                        number(qty),
                        number(qty),
                        "bundle_" + bundle_id,
                        hint=fields[0],
                        alternatives=(room,),
                        quality=int(number(quality)),
                    )
                )
        metrics.append(
            metric(
                "bundle_" + bundle_id,
                fields[0],
                quantity if room_ids.get(room) in completed else done,
                quantity,
                missing,
            )
        )
    projects = ("Greenhouse", "Bridge", "Panning", "Minecarts", "Bus")
    prices = (35000, 25000, 20000, 15000, 40000)
    if joja:
        items = [
            ProgressItem(
                str(index),
                projects[index],
                0,
                1,
                1,
                "joja_project",
                cost=prices[index],
                cost_unit="gold",
            )
            for index in range(5)
            if index not in completed
        ]
    achievements = (
        metric(
            "local_legend",
            "Local Legend",
            int(not joja and cc_count >= 6 and ceremony),
            1,
            possible=not joja,
        ),
        metric(
            "joja_member_of_the_year",
            "Joja Co. Member of the Year",
            int(joja and ceremony),
            1,
            possible=joja or cc_count < 6,
        ),
    )
    return ProgressResult(
        "bundles",
        "Community Center / Joja Community Development",
        achievements + tuple(metrics),
        items=tuple(items),
        facts=facts(
            joja_member=joja,
            community_center_rooms=cc_count,
            joja_projects=len(joja_done),
            completed_rooms=tuple(
                room_names[index] for index in sorted(completed) if index in room_names
            ),
            attended_ceremony=ceremony,
        ),
    )


def raccoons(ctx):
    fed = integer(ctx.root, "timesFedRaccoons")
    last = integer(ctx.root, "daysPlayedWhenLastRaccoonBundleWasFinished")
    days = ctx.stats[ctx.host_id].get("daysPlayed", 0) - last
    flags = ctx.mail[ctx.host_id]
    phase = (
        "moved_in"
        if "raccoonMovedIn" in flags
        else "tree_fallen"
        if "raccoonTreeFallen" in flags
        else "greenhouse_repaired"
        if {"ccPantry", "jojaPantry"} & flags
        else "greenhouse_needed"
    )
    complete = fed > 9 or fed == 9 and days > 7
    return ProgressResult(
        "raccoons",
        "Forest Neighbors",
        (metric("good_neighbors", "Good Neighbors", int(complete), 1),),
        facts=facts(
            times_fed=fed,
            last_fed_day=last,
            days_since_fed=days,
            phase=phase,
            next_request_wait_days=max(0, 8 - days),
        ),
    )


def animals(ctx):
    items = []
    buildings = []
    for location in ctx.locations():
        for npc in location.findall(".//NPC"):
            if object_type(npc) in ("Pet", "Cat", "Dog"):
                love = integer(npc, "friendshipTowardFarmer")
                items.append(
                    ProgressItem(
                        value(npc, "petId") or value(npc, "name", ""),
                        value(npc, "name", ""),
                        love,
                        1000,
                        max(0, 1000 - love),
                        "pet",
                        kind=value(npc, "petType", object_type(npc)),
                    )
                )
        for building in location.findall("buildings/Building"):
            kind = value(building, "buildingType", "")
            if kind not in (
                "Coop",
                "Big Coop",
                "Deluxe Coop",
                "Barn",
                "Big Barn",
                "Deluxe Barn",
            ):
                continue
            buildings.append(
                (
                    kind,
                    integer(building, "currentOccupants"),
                    integer(building, "maxOccupants"),
                )
            )
            for animal in building.findall(
                "indoors/Animals/SerializableDictionaryOfInt64FarmAnimal//FarmAnimal"
            ) or building.findall("indoors/animals//FarmAnimal"):
                kind = value(animal, "type", "")
                cracker = value(animal, "hasEatenAnimalCracker") == "true"
                items.append(
                    ProgressItem(
                        value(animal, "myID") or value(animal, "name", ""),
                        value(animal, "name", ""),
                        int(cracker),
                        1,
                        int(not cracker),
                        "farm_animal",
                        kind=kind,
                        status="cannot_eat_cracker"
                        if kind == "Pig"
                        else "has_eaten_cracker"
                        if cracker
                        else "has_not_eaten_cracker",
                    )
                )
    return ProgressResult(
        "animals",
        "Animal Summary",
        items=tuple(items),
        facts=facts(buildings=tuple(buildings)),
    )
