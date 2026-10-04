"""Player skills, combat, family, relationships, powers and milestones."""

from .common import counts, dictionary, integer, number, object_type, value, values
from .models import ProgressItem, ProgressResult, facts, metric

SKILLS = ("Farming", "Fishing", "Foraging", "Mining", "Combat")
LEVEL_XP = (100, 380, 770, 1300, 2150, 3300, 4800, 6900, 10000, 15000)
MASTERY_XP = (10000, 25000, 45000, 70000, 100000)


def skills(ctx, mastery=False):
    players = []
    for player in ctx.players:
        key, node = ctx.player_id(player), player.snapshot
        xp = [number(x) for x in values(node, "experiencePoints/int")]
        xp += [0] * (5 - len(xp))
        maxed = sum(x >= 15000 for x in xp[:5])
        level = sum(
            integer(node, skill.lower() + "Level") for skill in SKILLS
        ) + integer(node, "luckLevel")
        level //= 2
        metrics = [
            metric("maxed_skills", "Master of the Five Ways", maxed, 5),
            metric("singular_talent", "Singular Talent", maxed, 1),
        ]
        items = [
            ProgressItem(
                skill.lower(),
                skill,
                xp[i],
                15000,
                max(0, 15000 - xp[i]),
                "skill",
                level=sum(xp[i] >= threshold for threshold in LEVEL_XP),
                next_goal=next(
                    (threshold for threshold in LEVEL_XP if threshold > xp[i]), None
                ),
                next_missing=next(
                    (threshold - xp[i] for threshold in LEVEL_XP if threshold > xp[i]),
                    0,
                ),
            )
            for i, skill in enumerate(SKILLS)
        ]
        ctx.perfection[key]["skills"] = (level, 25)
        titles = (
            "Newcomer",
            "Greenhorn",
            "Bumpkin",
            "Cowpoke",
            "Farmhand",
            "Tiller",
            "Smallholder",
            "Sodbuster",
            "Farmboy" if value(node, "isMale") == "true" else "Farmgirl",
            "Granger",
            "Planter",
            "Rancher",
            "Farmer",
            "Agriculturist",
        )
        title = (
            titles[max(0, (level - 1) // 2)]
            if level < 29
            else "Cropmaster"
            if level == 29
            else "Farm King"
        )
        detail = facts(farmer_level=level, farmer_title=title)
        if mastery:
            stats = ctx.stats[key]
            mastery_xp = stats.get("MasteryExp", 0)
            unlocked = sum(mastery_xp >= threshold for threshold in MASTERY_XP)
            selected = sum("mastery_" + str(i) in stats for i in range(5))
            items = [
                ProgressItem(
                    "mastery_" + str(i),
                    skill,
                    int("mastery_" + str(i) in stats),
                    1,
                    int("mastery_" + str(i) not in stats),
                    "mastery",
                )
                for i, skill in enumerate(SKILLS)
            ]
            metrics = [
                metric("mastery_cave", "Gain access to the Mastery Cave", maxed, 5),
                metric("mastery_experience", "Mastery experience", mastery_xp, 100000),
                metric(
                    "mastery_perks",
                    "Acquire all mastery perks",
                    selected,
                    5,
                    (x.item_id for x in items if x.missing),
                ),
            ]
            detail = facts(
                unlocked_perks=unlocked,
                available_unselected_perks=max(0, unlocked - selected),
                next_unlock_experience=next(
                    (threshold for threshold in MASTERY_XP if threshold > mastery_xp),
                    None,
                ),
            )
        players.append(ctx.player_result(player, metrics, items, detail))
    return ProgressResult(
        "skill_mastery" if mastery else "skills",
        "Skill Mastery" if mastery else "Skills",
        players=tuple(players),
    )


def quests(ctx):
    return ProgressResult(
        "quests",
        "Quests",
        players=tuple(
            ctx.player_result(
                p,
                (
                    metric(
                        "gofer",
                        "Gofer",
                        ctx.stats[ctx.player_id(p)].get("questsCompleted", 0),
                        10,
                    ),
                    metric(
                        "a_big_help",
                        "A Big Help",
                        ctx.stats[ctx.player_id(p)].get("questsCompleted", 0),
                        40,
                    ),
                ),
            )
            for p in ctx.players
        ),
    )


def monsters(ctx):
    goals = {
        "Slimes": 1000,
        "Void Spirits": 150,
        "Bats": 200,
        "Skeletons": 50,
        "Cave Insects": 125,
        "Duggies": 30,
        "Dust Sprites": 500,
    }
    categories = dict(ctx.catalog("monster_categories"))
    members = {k: list(v) for k, v in ctx.catalog("monster_members").items()}
    if ctx.version >= (1, 4, 0):
        goals.update(
            {"Rock Crabs": 60, "Mummies": 100, "Pepper Rex": 50, "Serpents": 250}
        )
        members.update(
            {
                "Rock Crabs": ["Rock Crab", "Lava Crab", "Iridium Crab"],
                "Mummies": ["Mummy"],
                "Pepper Rex": ["Pepper Rex"],
                "Serpents": ["Serpent"],
            }
        )
    if ctx.version >= (1, 5, 0):
        goals["Flame Spirits"] = 150
        members["Flame Spirits"] = ["Magma Sprite", "Magma Sparker"]
        for category, monster in [
            ("Slimes", "Tiger Slime"),
            ("Void Spirits", "Shadow Sniper"),
            ("Duggies", "Magma Duggy"),
            ("Bats", "Iridium Bat"),
            ("Serpents", "Royal Serpent"),
            ("Skeletons", "Skeleton Mage"),
        ]:
            members[category].append(monster)
    if ctx.version >= (1, 4, 0):
        categories.update(
            {
                "Rock Crab": "Rock Crabs",
                "Lava Crab": "Rock Crabs",
                "Iridium Crab": "Rock Crabs",
                "Mummy": "Mummies",
                "Pepper Rex": "Pepper Rex",
                "Serpent": "Serpents",
            }
        )
    if ctx.version >= (1, 5, 0):
        categories.update(
            {
                "Magma Sprite": "Flame Spirits",
                "Magma Sparker": "Flame Spirits",
                "Tiger Slime": "Slimes",
                "Shadow Sniper": "Void Spirits",
                "Magma Duggy": "Duggies",
                "Iridium Bat": "Bats",
                "Royal Serpent": "Serpents",
            }
        )
    if ctx.version >= (1, 6, 0):
        goals["Cave Insects"] = 80
    players = []
    for player in ctx.players:
        key, node = ctx.player_id(player), player.snapshot
        base = ctx.root if ctx.version < (1, 3, 0) else node
        raw = counts(base, "stats/specificMonstersKilled")
        killed = {
            category: sum(
                count
                for monster, count in raw.items()
                if categories.get(monster) == category and count > 0
            )
            for category in goals
        }
        done = sum(killed[k] >= goal for k, goal in goals.items())
        items = tuple(
            ProgressItem(
                k,
                k,
                killed[k],
                goal,
                max(0, goal - killed[k]),
                "monster_goal",
                alternatives=tuple(members[k]),
            )
            for k, goal in goals.items()
        )
        depth = integer(node, "deepestMineLevel")
        if value(node, "hasSkullKey") == "true":
            depth = max(depth, 120)
        total = ctx.stats[key].get("monstersKilled", 0)
        metrics = [
            metric(
                "protector_of_the_valley",
                "Protector of the Valley",
                done,
                len(goals),
                (x.item_id for x in items if x.missing),
            ),
            metric("the_bottom", "The Bottom", depth, 120),
        ]
        if ctx.version >= (1, 6, 0):
            metrics.append(
                metric(
                    "adventure_guild_back_room",
                    "Gain access to the Adventure Guild back room",
                    total,
                    1000,
                )
            )
        ctx.perfection[key]["monsters"] = (int(done >= len(goals)), 1)
        players.append(
            ctx.player_result(
                player,
                metrics,
                items,
                facts(deepest_mine_level=depth, total_monsters_killed=total),
            )
        )
    return ProgressResult("monsters", "Monster Hunting", players=tuple(players))


def stardrops(ctx):
    catalog = ctx.catalog("stardrops")
    players = []
    for player in ctx.players:
        key = ctx.player_id(player)
        consumed = dictionary(player.snapshot, "chestConsumedLevels")
        found = {
            flag
            for flag in catalog
            if flag in ctx.mail[key]
            or flag == "CF_Mines"
            and consumed.get("100") == "true"
        }
        override = "gotMaxStamina" in ctx.mail[key]
        missing = tuple(
            ProgressItem(flag, description, 0, 1, 1, "stardrop")
            for flag, description in catalog.items()
            if flag not in found
        )
        ctx.perfection[key]["stardrops"] = (
            int(override or len(found) >= len(catalog)),
            1,
        )
        players.append(
            ctx.player_result(
                player,
                (
                    metric(
                        "stardrops",
                        "Mystery of the Stardrops",
                        len(found),
                        len(catalog),
                        (x.item_id for x in missing),
                    ),
                ),
                missing,
                facts(
                    max_stamina=integer(player.snapshot, "maxStamina"),
                    stamina_override=override,
                ),
            )
        )
    return ProgressResult("stardrops", "Stardrops", players=tuple(players))


def friendship_entries(ctx, node):
    result = {}
    if ctx.version >= (1, 3, 0):
        for entry in node.findall("friendshipData/item"):
            name = value(entry, "key/string", "")
            status = value(entry, "value/Friendship/Status", "Friendly")
            if (
                status == "Married"
                and value(entry, "value/Friendship/RoommateMarriage") == "true"
            ):
                status = "Roommate"
            result[name] = (integer(entry, "value/Friendship/Points"), status)
    else:
        for entry in node.findall("friendships/item"):
            result[value(entry, "key/string", "")] = (
                integer(entry, "value/ArrayOfInt/int"),
                "Friendly",
            )
    return result


def social(ctx):
    ignore = set(ctx.catalog("social_ignore"))
    events = ctx.updated_catalog("friendship_events", "social")
    npcs = {}
    legacy_status = {}
    for location in ctx.locations():
        for npc in location.findall(".//NPC"):
            name = value(npc, "name", "")
            kind = object_type(npc)
            if name not in ignore and kind not in ignore:
                npcs[name] = (
                    value(npc, "datable") == "true",
                    kind == "Child",
                    value(npc, "gender") == "1",
                )
                legacy_status[name] = (
                    "Divorced"
                    if value(npc, "divorcedFromFarmer") == "true"
                    else "Married"
                    if integer(npc, "daysMarried") > 0
                    else "Dating"
                    if value(npc, "datingFarmer") == "true"
                    else "Friendly"
                )
    players = []
    for player in ctx.players:
        key, node = ctx.player_id(player), player.snapshot
        raw = friendship_entries(ctx, node)
        eligible = {
            name: rel
            for name, rel in raw.items()
            if name in npcs and name not in ignore
        }
        achievement_relationships = eligible if ctx.version >= (1, 3, 0) else raw
        count5 = sum(pts >= 1250 for pts, _ in achievement_relationships.values())
        count10 = sum(pts >= 2500 for pts, _ in achievement_relationships.values())
        max_total = sum(name in events for name in eligible)
        max_count = sum(
            pts >= (2000 if npcs[name][0] else 2500)
            for name, (pts, _) in eligible.items()
            if name in events
        )
        spouse = value(node, "spouse", "")
        if ctx.version < (1, 3, 0) and integer(ctx.root, "countdownToWedding") > 0:
            spouse = spouse[:-7]
        items = []
        for name, (datable, child, is_girl) in npcs.items():
            pts, status = eligible.get(name, (0, "Unmet"))
            if ctx.version < (1, 3, 0) and name in eligible:
                status = (
                    "Engaged"
                    if name == spouse and integer(ctx.root, "countdownToWedding") > 0
                    else legacy_status[name]
                )
            goal = (
                (
                    3500
                    if ctx.version >= (1, 4, 0)
                    else 3250
                    if "CF_Spouse" in ctx.mail[key]
                    else 3375
                )
                if name == spouse
                else 2500
                if not datable or status == "Dating"
                else 2000
            )
            items.append(
                ProgressItem(
                    name,
                    name,
                    pts,
                    goal,
                    max(0, goal - pts),
                    "spouse"
                    if name == spouse
                    else "child"
                    if child
                    else "datable"
                    if datable
                    else "villager",
                    hearts=pts // 250,
                    status=status,
                )
            )
            for hearts, event in sorted(
                events.get(name, ()), key=lambda event: number(event[0])
            ):
                event_ids = str(event).split("|")
                seen = any(event_id in ctx.events[key] for event_id in event_ids)
                possible = not (
                    (event == 101 and {"2123243", "2123343"} & ctx.events[key])
                    or (event == 733330 and ctx.stats[key].get("daysPlayed", 0) > 84)
                    or (
                        event == 35
                        and "pamHouseUpgrade" in ctx.mail[key]
                        and ctx.version < (1, 5, 0)
                    )
                    or (
                        event == 36
                        and "pamHouseUpgrade" in ctx.mail[key]
                        and ctx.version < (1, 4, 0)
                    )
                    or (number(hearts) == 10 and datable and status == "Friendly")
                    or (number(hearts) >= 14 and name != spouse)
                )
                items.append(
                    ProgressItem(
                        str(event),
                        f"{name}: {hearts} hearts",
                        int(seen),
                        1,
                        int(not seen),
                        "friendship_event",
                        hearts=number(hearts),
                        status="seen"
                        if seen
                        else "available"
                        if possible
                        else "impossible",
                        event_ids=tuple(event_ids),
                    )
                )
        introductions = tuple(
            name
            for quest in node.findall("questLog/*")
            if object_type(quest) == "SocializeQuest"
            for name in values(quest, "whoToGreet/string")
        )
        goals = [
            (
                "introductions",
                "Complete Introductions quest",
                int(not introductions),
                1,
            ),
            ("a_new_friend", "A New Friend", count5, 1),
            ("best_friends", "Best Friends", count10, 1),
            ("the_beloved_farmer", "The Beloved Farmer", count10, 8),
            ("cliques", "Cliques", count5, 4),
            ("networking", "Networking", count5, 10),
            ("popular", "Popular", count5, 20),
            ("great_friends", "Great Friends", max_count, max_total),
        ]
        ctx.perfection[key]["great_friends"] = (max_count, max_total)
        players.append(
            ctx.player_result(
                player,
                tuple(metric(*goal) for goal in goals),
                items,
                facts(
                    introductions_remaining=introductions,
                    spouse=spouse,
                    has_spouse_stardrop="CF_Spouse" in ctx.mail[key],
                    all_bachelors_event=bool({"195013", "195099"} & ctx.events[key]),
                    all_bachelorettes_event=bool(
                        {"195012", "195019"} & ctx.events[key]
                    ),
                ),
            )
        )
    return ProgressResult("social", "Social", players=tuple(players))


def family(ctx):
    children = {ctx.host_id: []}
    for location in ctx.locations():
        interiors = [location] + list(location.findall(".//indoors"))
        for house in interiors:
            kind = object_type(house)
            if kind not in ("FarmHouse", "Cabin"):
                continue
            for npc in house.findall(".//NPC"):
                if object_type(npc) != "Child":
                    continue
                owner = (
                    value(npc, "idOfParent")
                    or value(house, "owner/UniqueMultiplayerID")
                    or value(house, "owner")
                    or ctx.host_id
                )
                children.setdefault(owner, []).append(value(npc, "name", ""))
    players = []
    names = {ctx.player_id(player): player.name for player in ctx.players}
    for player in ctx.players:
        key, node = ctx.player_id(player), player.snapshot
        spouse = player.spouse or names.get(ctx.partners.get(key), "")
        kids = tuple(
            dict.fromkeys(
                children.get(key, []) or children.get(ctx.partners.get(key), [])
            )
        )
        upgrades = player.house_upgrade_level or 0
        goals = [
            metric("full_house", "Full House", int(bool(spouse)) + len(kids), 3),
            metric("moving_up", "Moving Up", upgrades, 1),
            metric("living_large", "Living Large", upgrades, 2),
            metric(
                "house_fully_upgraded",
                "House fully upgraded",
                upgrades,
                3 if key == ctx.host_id else 2,
            ),
        ]
        players.append(
            ctx.player_result(
                player,
                goals,
                detail=facts(
                    spouse=spouse or None,
                    children=kids,
                    wedding_countdown=integer(ctx.root, "countdownToWedding"),
                ),
            )
        )
    return ProgressResult("family", "Home and Family", players=tuple(players))


def powers(ctx):
    groups = (("book_powers", "books"), ("special_powers", "special"))
    names = {**ctx.catalog("object_names"), **ctx.catalog("power_names")}
    players = []

    def owns(key, condition, book):
        fields = condition.split()
        source = (
            ctx.stats[key]
            if fields[0] == "PLAYER_STAT"
            else ctx.events[key]
            if fields[0] == "PLAYER_HAS_SEEN_EVENT"
            else ctx.mail[key]
        )
        if fields[2] not in source:
            return False
        if fields[0] == "PLAYER_STAT":
            return (
                source[fields[2]] >= number(fields[3], 1)
                if book
                else source[fields[2]] == number(fields[3], 1)
            )
        return True

    for player in ctx.players:
        key = ctx.player_id(player)
        items = []
        metrics = []
        for name, category in groups:
            catalog = ctx.catalog(name)
            have = 0
            missing = []
            for power, condition in catalog.items():
                fields = condition.split()
                owned = (
                    fields[1] == "Host"
                    and owns(ctx.host_id, condition, category == "books")
                ) or owns(key, condition, category == "books")
                have += int(owned)
                if not owned:
                    missing.append(power)
                    items.append(
                        ProgressItem(power, names.get(power, power), 0, 1, 1, category)
                    )
            metrics.append(
                metric(
                    category,
                    "Well-read"
                    if category == "books"
                    else "Acquire all special items and powers",
                    have,
                    len(catalog),
                    missing,
                )
            )
        players.append(ctx.player_result(player, metrics, items))
    return ProgressResult(
        "powers", "Books, Special Items & Powers", players=tuple(players)
    )


def arcade(ctx):
    players = []
    for player in ctx.players:
        key, node = ctx.player_id(player), player.snapshot
        saved = node.find("JOTPKProgress")
        stage = integer(saved, "whichRound/int") + 1 if saved is not None else None
        wave = integer(saved, "whichWave/int") + 1 if saved is not None else None
        completed = (
            (8 if stage == 3 else (4 if stage == 2 else -1) + wave) if stage else 0
        )
        players.append(
            ctx.player_result(
                player,
                (
                    metric(
                        "prairie_king",
                        "Journey of the Prairie King",
                        int("Beat_PK" in ctx.mail[key]),
                        1,
                    ),
                    metric(
                        "junimo_kart",
                        "Junimo Kart",
                        int("JunimoKart" in ctx.mail[key]),
                        1,
                    ),
                ),
                detail=facts(
                    prairie_king_stage=stage,
                    prairie_king_wave=wave,
                    prairie_king_stages_completed=completed,
                    prairie_king_deathless=value(saved, "died/boolean") != "true"
                    if saved is not None
                    else None,
                ),
            )
        )
    leaders = tuple(
        ProgressItem(
            str(index),
            value(entry, "name/*", ""),
            integer(entry, "score/*"),
            category="junimo_kart_leaderboard",
        )
        for index, entry in enumerate(
            ctx.root.findall("junimoKartLeaderboards/entries/NetLeaderboardsEntry")
        )
    )
    return ProgressResult(
        "arcade_games", "Arcade Games", players=tuple(players), items=leaders
    )
