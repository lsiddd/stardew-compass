"""Prize tickets rules adapted from MouseyPounds (MIT; predictor b9e7c71)."""

from ..report_support import (
    PredictionContext,
    SystemRandom,
    capture,
    exact_seed_part,
    floor,
    fmod,
    random_seed,
)


def predict_prize_ticket(
    context: PredictionContext, is_search: bool | None = None, offset: int | None = None
) -> None:
    save = context.save
    page_size = context.count or 20
    which_player = context.player_index
    if offset is None:
        offset = page_size * floor(
            save.get("ticketPrizesClaimed")[int(which_player)] / page_size
        )
    if not save.get("mp_ids") is None:
        rng = SystemRandom(
            random_seed(
                exact_seed_part(int(save.get("gameID"))),
                exact_seed_part(save.get("mp_ids")[int(which_player)]),
                legacy=save["useLegacyRandom"],
            )
        )
    else:
        rng = SystemRandom(
            random_seed(save.get("gameID"), 0, legacy=save["useLegacyRandom"])
        )
    rand_roll = rng.double()
    g = 1
    while g <= page_size:
        num_opened = offset + g
        prize_level = num_opened - 1
        item, item_qty = _prize_contents(save, prize_level, rand_roll)
        capture(
            context,
            "predictPrizeTicket",
            {
                "numOpened": num_opened,
                "whichPlayer": which_player,
                "item": item,
                "itemQty": item_qty,
                "prizeLevel": prize_level,
            },
        )
        g += 1
    return None


def _prize_contents(save, prize_level, rand_roll):
    item = ""
    item_qty = 1
    match prize_level:
        case 0:
            item = "Raccoon Seeds"
            item_qty = 12
        case 1:
            item = "Peach Sapling" if rand_roll < 0.5 else "Orange Sapling"
        case 2:
            if rand_roll < 0.5:
                item = "Mixed Seeds"
                item_qty = 10
            else:
                item = "Mixed Flower Seeds"
                item_qty = 15
        case 3:
            item = "Mystery Box"
            item_qty = 3
        case 15 | 4:
            item = "Stardrop Tea"
        case 5:
            item = "Blue Pinstripe Bed"
        case 6:
            match floor(3 * rand_roll):
                case 0:
                    item = "Quality Sprinkler"
                case 1:
                    item = "Preserves Jar"
                case 2:
                    item = "Mushroom Log"
            item_qty = 4
        case 7:
            item = "Apple Sapling" if rand_roll < 0.5 else "Pomegranate Sapling"
        case 8:
            item = "Friendship 101"
        case 9:
            match floor(3 * rand_roll):
                case 0:
                    item = "Cherry Bomb"
                    item_qty = 20
                case 1:
                    item = "Bomb"
                    item_qty = 12
                case 2:
                    item = "Mega Bomb"
                    item_qty = 6
        case 10:
            item = "Sports Cap"
        case 11:
            item = "Fish Smoker" if rand_roll < 0.5 else "Dehydrator"
        case 12:
            item = "Artifact Trove" if rand_roll < 0.5 else "Mystery Box"
            item_qty = 4
        case 13:
            choice = ["House Plant (1)", "House Plant (2)", "House Plant (3)"]
            item = choice[int(floor(rand_roll * len(choice)))]
        case 14:
            choice = [
                "Stardew Valley Almanac",
                "Bait And Bobber",
                "Woodcutter's Weekly",
                "Mining Monthly",
                "Combat Quarterly",
            ]
            item = f"{choice[int(floor(rand_roll * len(choice)))]}"
        case 16:
            item = "Cow Decal"
        case 17:
            item = "Omni Geode"
            item_qty = 8
        case 18:
            item = "Bee House" if rand_roll < 0.5 else "Keg"
            item_qty = 4
        case 19:
            item = "Diamond"
            item_qty = 5
        case 20:
            item = "Mystery Box"
            item_qty = 5
        case 21:
            item = "Magic Rock Candy"
        case _:
            return _recurring_prize(save, prize_level)
    return (item, item_qty)


def _recurring_prize(save, prize_level):
    item = ""
    item_qty = 1
    rng2 = SystemRandom(
        random_seed(
            save.get("gameID"),
            prize_level - fmod(prize_level, 9),
            legacy=save["useLegacyRandom"],
        )
    )
    match fmod(prize_level, 9):
        case 0:
            item = "Mystery Box"
            item_qty = 5
        case 1:
            item = "Fairy Dust"
            item_qty = rng2.next(1, 3)
        case 2:
            choice = [
                "Iridium Bar",
                "Spicy Eel",
                "Triple Shot Espresso",
                "Crab Cakes",
                "Artifact Trove",
            ]
            item = choice[int(rng2.next(len(choice)))]
            item_qty = 5
        case 3:
            choice = ["House Plant (1)", "House Plant (2)", "House Plant (3)"]
            item = choice[int(rng2.next(len(choice)))]
        case 4:
            item = "Stardrop Tea"
        case 5:
            item = "Treasure Chest"
        case 6:
            item = "Iridium Sprinkler"
        case 7:
            choice = [
                "Fancy House Plant (1)",
                "Fancy House Plant (2)",
                "Fancy House Plant (3)",
                "Pig Painting",
            ]
            item = choice[int(rng2.next(len(choice)))]
        case 8:
            match rng2.next(2):
                case 0:
                    item = "Bomb"
                    item_qty = 15
                case 1:
                    item = "Mega Bomb"
                    item_qty = 8
        case _:
            item = "Mystery Box"
            item_qty = 5
    return (item, item_qty)
