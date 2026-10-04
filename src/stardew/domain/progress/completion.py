"""Grandpa scoring and category-wise multiplayer perfection aggregation."""

from .common import integer, object_type, value, values
from .models import ProgressItem, ProgressResult, facts, metric
from .player import SKILLS, friendship_entries


def grandpa(ctx):
    node = ctx.players[0].snapshot
    flags, events = ctx.mail[ctx.host_id], ctx.events[ctx.host_id]
    money = ctx.players[0].total_money_earned or 0
    earnings_points = next(
        (
            points
            for goal, points in (
                (1000000, 7),
                (500000, 5),
                (300000, 4),
                (200000, 3),
                (100000, 2),
                (50000, 1),
            )
            if money >= goal
        ),
        0,
    )
    achievements = ctx.players[0].achievements
    achievement_points = len(achievements & {"5", "26", "34"})
    ceremony = "191393" in events
    cc_complete = set(ctx.catalog("bundle_rooms")) <= flags
    cc_points = 3 if ceremony else int(cc_complete)
    keys = (
        (int("HasRustyKey" in flags), int("HasSkullKey" in flags))
        if ctx.version >= (1, 6, 0)
        else (
            int(value(node, "hasRustyKey") == "true"),
            int(value(node, "hasSkullKey") == "true"),
        )
    )
    spouse = ctx.players[0].spouse or ctx.partners.get(ctx.host_id)
    house = ctx.players[0].house_upgrade_level or 0
    family_points = int(bool(spouse) and house >= 2)
    friendships = friendship_entries(ctx, node)
    friends = sum(pts >= 1975 for pts, _ in friendships.values())
    friend_points = 2 if friends >= 10 else 1 if friends >= 5 else 0
    level = sum(integer(node, skill.lower() + "Level") for skill in SKILLS) + integer(
        node, "luckLevel"
    )
    level /= 2
    skill_points = 2 if level >= 25 else 1 if level >= 15 else 0
    pets = tuple(
        npc
        for location in ctx.locations()
        for npc in location.findall(".//NPC")
        if object_type(npc) in ("Pet", "Cat", "Dog")
    )
    love = max((integer(pet, "friendshipTowardFarmer") for pet in pets), default=0)
    if ctx.version >= (1, 6, 0) and "petLoveMessage" in flags:
        love = 1000
    pet_points = int(love >= 999)
    total = (
        earnings_points
        + achievement_points
        + cc_points
        + sum(keys)
        + family_points
        + friend_points
        + skill_points
        + pet_points
    )
    candles = 4 if total >= 12 else 3 if total >= 8 else 2 if total >= 4 else 1
    current = max(
        (integer(farm, "grandpaScore") for farm in ctx.locations("Farm")), default=0
    )
    milestones = [
        metric("grandpa_score", "Grandpa's evaluation points", total, 21),
        metric("four_candles", "Four candles", total, 12),
    ]
    categories = (
        ("earnings", earnings_points, 7),
        ("achievements", achievement_points, 3),
        ("community_center", cc_points, 3),
        ("keys", sum(keys), 2),
        ("family", family_points, 1),
        ("friendships", friend_points, 2),
        ("skills", skill_points, 2),
        ("pet", pet_points, 1),
    )
    milestones.extend(
        metric(key, key.replace("_", " ").title(), count, goal)
        for key, count, goal in categories
    )
    return ProgressResult(
        "grandpa",
        "Grandpa's Evaluation",
        tuple(milestones),
        facts=facts(
            predicted_candles=candles,
            current_candles=current,
            friendships_over_1975_points=friends,
            farmer_level=level,
            pet_friendship=love,
            has_pet=bool(pets),
            rusty_key=bool(keys[0]),
            skull_key=bool(keys[1]),
            joja_member="JojaMember" in flags,
        ),
    )


def perfection(ctx):
    weights = {
        "shipping": 15,
        "great_friends": 11,
        "cooking": 10,
        "crafting": 10,
        "fishing": 10,
        "skills": 5,
        "monsters": 10,
        "stardrops": 10,
    }
    names = {key: key.replace("_", " ").title() for key in weights}
    metrics = []
    diagnostics = []
    for category, weight in weights.items():
        best_key = None
        best_count, best_total = 0, 1
        best_ratio = -1.0
        for key, stats in ctx.perfection.items():
            count, total = stats.get(category, (0, 1))
            ratio = min(1, count / total) if total else 0
            if ratio > best_ratio:
                best_key, best_count, best_total, best_ratio = key, count, total, ratio
        metrics.append(
            metric(
                category,
                names[category],
                best_count,
                best_total,
                player_id=best_key,
                weight=weight,
            )
        )
        if not best_total:
            diagnostics.append(
                f"{names[category]} has no tracked targets and contributes 0% to perfection."
            )
    buildings = {
        value(building, "buildingType", "")
        for location in ctx.locations("Farm")
        for building in location.findall("buildings/Building")
    }
    obelisks = ("Earth Obelisk", "Water Obelisk", "Desert Obelisk", "Island Obelisk")
    missing = tuple(
        ProgressItem(name, name, 0, 1, 1, "perfection_building")
        for name in obelisks + ("Gold Clock",)
        if name not in buildings
    )
    metrics.append(
        metric(
            "obelisks",
            "Obelisks",
            sum(name in buildings for name in obelisks),
            4,
            tuple(name for name in obelisks if name not in buildings),
            weight=4,
        )
    )
    metrics.append(
        metric("gold_clock", "Gold Clock", int("Gold Clock" in buildings), 1, weight=10)
    )
    count, total = getattr(
        ctx, "walnut_progress", (integer(ctx.root, "goldenWalnutsFound"), 130)
    )
    metrics.append(metric("walnuts", "Golden Walnuts", count, total, weight=5))
    raw = sum(m.earned or 0 for m in metrics)
    waivers = (
        (ctx.state.world.perfection_waivers or 0) if ctx.version >= (1, 6, 0) else 0
    )
    adjusted = min(100, raw + waivers)
    return ProgressResult(
        "perfection_tracker",
        "Perfection Tracker",
        tuple(metrics) + (metric("perfection", "Perfection", adjusted, 100),),
        items=missing,
        facts=facts(
            raw_percentage=raw,
            adjusted_percentage=adjusted,
            perfection_waivers=waivers,
            percentage_remaining=max(0, 100 - adjusted),
        ),
        diagnostics=tuple(diagnostics),
    )
