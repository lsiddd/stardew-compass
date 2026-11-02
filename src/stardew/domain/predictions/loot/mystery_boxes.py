"""Mystery boxes rules adapted from MouseyPounds (MIT; predictor b9e7c71)."""

from ..report_support import PredictionContext, SystemRandom, capture, floor, set_slot
from .seasonal_seeds import low_grade_seeds, raccoon_seeds
from .seeds import player_sequence_seed
from .selection import set_object


def predict_mystery_boxes(
    context: PredictionContext, is_search: bool | None = None, offset: int | None = None
) -> None:
    save = context.save
    item_ids = []
    page_size = context.count or 20
    num_columns = 3
    which_player = context.player_index
    if offset is None:
        offset = page_size * floor(
            save.get("mysteryBoxesOpened")[int(which_player)] / page_size
        )
    c = 0
    g = 1
    while g <= page_size:
        num_opened = offset + g
        item = ["None", "None", "None"]
        item_ids = [None, None, None]
        item_qty = [1, 1, 1]
        no_link = [False, False, False]
        based_on_skill = [False, False, False]
        c = 0
        while c < num_columns:
            _box_contents(
                save,
                num_opened,
                which_player,
                c,
                item,
                item_ids,
                item_qty,
                no_link,
                based_on_skill,
            )
            c += 1
        c = 0
        while c < num_columns:
            seed_result = None
            alternatives = ()
            certainty = "saved_state"
            if item[c] == "Seasonal Seeds":
                alternatives = low_grade_seeds(
                    save.get("daysPlayed"), item_qty[c], save["objects"]
                )
                certainty = "session_dependent"
            elif item[c] == "Raccoon Seeds":
                seed_result, alternatives = raccoon_seeds(
                    save.get("daysPlayed"), item_qty[c]
                )
                certainty = "saved_date" if seed_result else "date_dependent"
            capture(
                context,
                "predictMysteryBoxes",
                {
                    "numOpened": num_opened,
                    "whichPlayer": which_player,
                    "c": c,
                    "item": item,
                    "itemQty": item_qty,
                    "itemIDs": item_ids,
                    "seedResult": seed_result,
                    "dropAlternatives": alternatives,
                    "certainty": certainty,
                    "openingRule": "Hypothetical opening on the saved date with the stated mastery scenario and saved skill/GotMysteryBook unchanged; later rows do not simulate prior rewards or a later season",
                    "requiresFishingLevel": 6 if based_on_skill[c] else None,
                    "farmingMasteryRequired": (c == 2) if c else None,
                    "matchesSavedMastery": (
                        save["hasFarmingMastery"] == (c == 2)
                        if c and save.get("hasFarmingMastery") is not None
                        else None
                    ),
                },
            )
            c += 1
        g += 1
    return None


def _box_contents(
    save, num_opened, which_player, c, item, item_ids, item_qty, no_link, based_on_skill
):
    rare_mod = 1 if c == 0 else 2
    extra_book_chance = 0 if save.get("gotMysteryBook") else 0.0004 * num_opened
    rng = SystemRandom(player_sequence_seed(save, num_opened, which_player))
    prewarm_amount2 = rng.next(1, 10)
    j = 0
    while j < prewarm_amount2:
        rng.double()
        j += 1
    prewarm_amount2 = rng.next(1, 10)
    i = 0
    while i < prewarm_amount2:
        rng.double()
        i += 1
    if num_opened > 10 or c > 0:
        _advanced_contents(
            save,
            rng,
            num_opened,
            c,
            item,
            item_ids,
            item_qty,
            no_link,
            based_on_skill,
            rare_mod,
            extra_book_chance,
        )
    if item[int(c)] == "None":
        _common_contents(
            save, rng, c, item, item_ids, item_qty, no_link, based_on_skill
        )


def _advanced_contents(
    save,
    rng,
    num_opened,
    c,
    item,
    item_ids,
    item_qty,
    no_link,
    based_on_skill,
    rare_mod,
    extra_book_chance,
):
    if c == 2 and rng.double() < 0.005:
        set_slot(item, c, "Golden Animal Cracker")
        set_slot(item_ids, c, "(O)GoldenAnimalCracker")
    elif c > 0 and rng.double() < 0.005:
        set_slot(item, c, "Auto-Petter")
        set_slot(item_ids, c, "(BC)272")
    elif rng.double() < 0.002 * rare_mod:
        set_object(save, item, item_ids, c, "_279")
    elif rng.double() < 0.004 * rare_mod:
        set_object(save, item, item_ids, c, "_74")
    elif rng.double() < 0.008 * rare_mod:
        set_object(save, item, item_ids, c, "_166")
    elif rng.double() < 0.01 * rare_mod + extra_book_chance:
        if not save.get("gotMysteryBook"):
            set_object(save, item, item_ids, c, "_Book_Mystery")
        else:
            choices = ["_PurpleBook", "_Book_Mystery"]
            set_object(
                save, item, item_ids, c, str(choices[int(rng.next(len(choices)))])
            )
    elif rng.double() < 0.01 * rare_mod:
        choices = ["_797", "_373"]
        set_object(save, item, item_ids, c, str(choices[int(rng.next(len(choices)))]))
    elif rng.double() < 0.01 * rare_mod:
        set_slot(item, c, "Mystery Hat")
        set_slot(item_ids, c, "(H)MysteryHat")
    elif rng.double() < 0.01 * rare_mod:
        set_slot(item, c, "Mystery Shirt")
        set_slot(item_ids, c, "(S)MysteryShirt")
    elif rng.double() < 0.01 * rare_mod:
        set_slot(item, c, "Mystery Wallpaper")
        set_slot(item_ids, c, "(WP)MoreWalls:11")
    elif rng.double() < 0.1 or c > 0:
        match rng.next(15):
            case 0:
                set_object(save, item, item_ids, c, "_288")
                set_slot(item_qty, c, 5)
            case 1:
                set_object(save, item, item_ids, c, "_253")
                set_slot(item_qty, c, 3)
            case 2:
                fishing_level = save.get("fishingLevel")
                if (fishing_level is None or fishing_level >= 6) and rng.double() < 0.5:
                    choices = ["_687", "_695"]
                    set_object(
                        save,
                        item,
                        item_ids,
                        c,
                        str(choices[int(rng.next(len(choices)))]),
                    )
                    set_slot(based_on_skill, c, fishing_level is None)
                else:
                    set_object(save, item, item_ids, c, "_242")
                    set_slot(item_qty, c, 2)
            case 3:
                set_object(save, item, item_ids, c, "_204")
                set_slot(item_qty, c, 2)
            case 4:
                set_object(save, item, item_ids, c, "_369")
                set_slot(item_qty, c, 20)
            case 5:
                set_object(save, item, item_ids, c, "_466")
                set_slot(item_qty, c, 20)
            case 6:
                set_object(save, item, item_ids, c, "_773")
                set_slot(item_qty, c, 2)
            case 7:
                set_object(save, item, item_ids, c, "_688")
                set_slot(item_qty, c, 3)
            case 8:
                set_object(save, item, item_ids, c, str(f"_{rng.next(628, 634)}"))
            case 9:
                set_slot(item, c, "Seasonal Seeds")
                set_slot(item_ids, c, None)
                set_slot(item_qty, c, 20)
                set_slot(no_link, c, True)
            case 10:
                if rng.double() < 0.5:
                    set_slot(item, c, "Ossified Blade")
                    set_slot(item_ids, c, "(W)60")
                else:
                    choices = ["_533", "_534"]
                    set_object(
                        save,
                        item,
                        item_ids,
                        c,
                        str(choices[int(rng.next(len(choices)))]),
                    )
            case 11:
                set_object(save, item, item_ids, c, "_621")
            case 12:
                set_slot(item, c, "Mystery Box")
                set_slot(item_ids, c, "(O)MysteryBox")
                set_slot(item_qty, c, rng.next(3, 5))
            case 13:
                set_object(save, item, item_ids, c, str(f"_SkillBook_{rng.next(5)}"))
            case 14:
                set_slot(item, c, "Raccoon Seeds")
                set_slot(item_ids, c, None)
                set_slot(item_qty, c, 8)
                set_slot(no_link, c, True)


def _common_contents(save, rng, c, item, item_ids, item_qty, no_link, based_on_skill):
    match rng.next(14):
        case 0:
            set_object(save, item, item_ids, c, "_395")
            set_slot(item_qty, c, 3)
        case 1:
            set_object(save, item, item_ids, c, "_287")
            set_slot(item_qty, c, 5)
        case 2:
            set_slot(item, c, "Seasonal Seeds")
            set_slot(item_ids, c, None)
            set_slot(item_qty, c, 8)
            set_slot(no_link, c, True)
        case 3:
            set_object(save, item, item_ids, c, str(f"_{rng.next(727, 734)}"))
        case 4:
            roll = 217
            while roll == 217:
                roll = rng.next(194, 240)
            set_object(save, item, item_ids, c, str(f"_{roll}"))
        case 5:
            set_object(save, item, item_ids, c, "_709")
            set_slot(item_qty, c, 10)
        case 6:
            set_object(save, item, item_ids, c, "_369")
            set_slot(item_qty, c, 10)
        case 7:
            set_object(save, item, item_ids, c, "_466")
            set_slot(item_qty, c, 10)
        case 8:
            set_object(save, item, item_ids, c, "_688")
        case 9:
            set_object(save, item, item_ids, c, "_689")
        case 10:
            set_object(save, item, item_ids, c, "_770")
            set_slot(item_qty, c, 10)
        case 11:
            set_slot(item, c, "Mixed Flower Seeds")
            set_slot(item_ids, c, "(O)MixedFlowerSeeds")
            set_slot(item_qty, c, 10)
        case 12:
            if rng.double() < 0.4:
                match rng.next(4):
                    case 0:
                        set_object(save, item, item_ids, c, "_525")
                    case 1:
                        set_object(save, item, item_ids, c, "_529")
                    case 2:
                        set_object(save, item, item_ids, c, "_888")
                    case _:
                        set_object(
                            save, item, item_ids, c, str(f"_{rng.next(531, 533)}")
                        )
            else:
                set_slot(item, c, "Mystery Box")
                set_slot(item_ids, c, "(O)MysteryBox")
                set_slot(item_qty, c, 2)
        case 13:
            set_object(save, item, item_ids, c, "_690")
        case _:
            set_object(save, item, item_ids, c, "_382")
